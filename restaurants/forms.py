"""Forms for the restaurant-owner dashboard."""

from django import forms
from django.utils.translation import gettext_lazy as _

from reviews.models import CommentReply

from .geo import get_all_city_choices, is_valid_palestine_coords
from .models import MenuCategory, MenuItem, Restaurant, RestaurantCategory, RestaurantImage
from .utils import (
    format_working_hours,
    parse_time_value,
    parse_working_hours,
)

_RD_INPUT = "rd-input"
_RD_TEXTAREA = "rd-input rd-textarea"


class RestaurantInfoForm(forms.ModelForm):
    """Edit core restaurant profile fields shown on the Info tab."""

    restaurant_type = forms.ModelChoiceField(
        queryset=RestaurantCategory.objects.all(),
        label=_("Restaurant Type"),
        required=False,
        empty_label=_("Select a type"),
        widget=forms.Select(attrs={"class": _RD_INPUT}),
    )
    opening_time = forms.TimeField(
        label=_("Opening Time"),
        required=False,
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={"type": "time", "class": f"{_RD_INPUT} rd-time-input"},
        ),
        input_formats=["%H:%M", "%H:%M:%S"],
    )
    closing_time = forms.TimeField(
        label=_("Closing Time"),
        required=False,
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={"type": "time", "class": f"{_RD_INPUT} rd-time-input"},
        ),
        input_formats=["%H:%M", "%H:%M:%S"],
    )
    cover_image = forms.ImageField(
        label=_("Cover Photo"),
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "rd-file", "accept": "image/*"}),
        help_text=_("Shown on your restaurant card and detail page."),
    )

    class Meta:
        model = Restaurant
        fields = (
            "name_en",
            "name_ar",
            "city",
            "address_en",
            "address_ar",
            "description_en",
            "description_ar",
            "latitude",
            "longitude",
        )
        widgets = {
            "name_en": forms.TextInput(
                attrs={"class": _RD_INPUT, "placeholder": _("e.g. Al-Kanaan")},
            ),
            "name_ar": forms.TextInput(
                attrs={"class": _RD_INPUT, "placeholder": _("e.g. الكنعان")},
            ),
            "address_en": forms.TextInput(
                attrs={"class": _RD_INPUT, "placeholder": _("Street, area, city")},
            ),
            "address_ar": forms.TextInput(
                attrs={"class": _RD_INPUT, "placeholder": _("الشارع، المنطقة، المدينة")},
            ),
            "description_en": forms.Textarea(
                attrs={"class": _RD_TEXTAREA, "rows": 4, "placeholder": _("About your restaurant")},
            ),
            "description_ar": forms.Textarea(
                attrs={"class": _RD_TEXTAREA, "rows": 4, "placeholder": _("نبذة عن مطعمك")},
            ),
            "latitude": forms.HiddenInput(attrs={"id": "rd-latitude-input"}),
            "longitude": forms.HiddenInput(attrs={"id": "rd-longitude-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["restaurant_type"].initial = self.instance.category_id
            hours = (
                self.instance.working_hours_en
                or self.instance.working_hours_ar
                or ""
            )
            opening, closing = parse_working_hours(hours)
            opening_time = parse_time_value(opening)
            closing_time = parse_time_value(closing)
            if opening_time:
                self.fields["opening_time"].initial = opening_time
            if closing_time:
                self.fields["closing_time"].initial = closing_time

        self.fields["name_en"].label = _("Name (English)")
        self.fields["name_ar"].label = _("Name (Arabic)")
        self.fields["city"] = forms.ChoiceField(
            label=_("City"),
            choices=[("", _("Select a city"))] + get_all_city_choices(),
            required=True,
        )
        if self.instance and self.instance.pk and self.instance.city:
            self.fields["city"].initial = self.instance.city
        self.fields["address_en"].label = _("Address (English)")
        self.fields["address_ar"].label = _("Address (Arabic)")
        self.fields["description_en"].label = _("Description (English)")
        self.fields["description_ar"].label = _("Description (Arabic)")
        self.fields["latitude"].label = _("Latitude")
        self.fields["longitude"].label = _("Longitude")
        self.fields["latitude"].required = False
        self.fields["longitude"].required = False

    def clean_latitude(self):
        latitude = self.cleaned_data.get("latitude")
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise forms.ValidationError(_("Latitude must be between -90 and 90."))
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get("longitude")
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise forms.ValidationError(_("Longitude must be between -180 and 180."))
        return longitude

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        if latitude is None and longitude is None:
            return cleaned_data

        if latitude is None or longitude is None:
            raise forms.ValidationError(
                _("Please pick a complete location on the map."),
            )

        if not is_valid_palestine_coords(latitude, longitude):
            raise forms.ValidationError(
                _("Location must be within Palestine (West Bank and Gaza)."),
            )

        return cleaned_data

    def save(self, commit=True):
        restaurant = super().save(commit=False)
        restaurant.category = self.cleaned_data.get("restaurant_type")
        hours = format_working_hours(
            self.cleaned_data.get("opening_time", ""),
            self.cleaned_data.get("closing_time", ""),
        )
        restaurant.working_hours_en = hours
        restaurant.working_hours_ar = hours
        if commit:
            restaurant.save()
        cover = self.cleaned_data.get("cover_image")
        if cover:
            primary = RestaurantImage.objects.filter(
                restaurant=restaurant,
                is_primary=True,
            ).first()
            if primary:
                primary.image = cover
                primary.image_type = RestaurantImage.ImageType.COVER
                primary.save()
            else:
                RestaurantImage.objects.create(
                    restaurant=restaurant,
                    image=cover,
                    image_type=RestaurantImage.ImageType.COVER,
                    is_primary=True,
                )
        return restaurant


class MenuItemForm(forms.ModelForm):
    """Create or update a menu item from the Menu tab."""

    class Meta:
        model = MenuItem
        fields = (
            "name_en",
            "name_ar",
            "description_en",
            "description_ar",
            "price",
            "image",
        )
        widgets = {
            "name_en": forms.TextInput(
                attrs={"class": _RD_INPUT, "placeholder": _("e.g. Musakhan")},
            ),
            "name_ar": forms.TextInput(
                attrs={"class": _RD_INPUT, "placeholder": _("e.g. مسخن")},
            ),
            "description_en": forms.Textarea(
                attrs={
                    "class": _RD_TEXTAREA,
                    "rows": 3,
                    "placeholder": _("Short description of the dish"),
                },
            ),
            "description_ar": forms.Textarea(
                attrs={
                    "class": _RD_TEXTAREA,
                    "rows": 3,
                    "placeholder": _("وصف قصير للطبق"),
                },
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": _RD_INPUT,
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "45.00",
                },
            ),
            "image": forms.ClearableFileInput(attrs={"class": "rd-file"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name_en"].label = _("Name (English)")
        self.fields["name_ar"].label = _("Name (Arabic)")
        self.fields["description_en"].label = _("Description (English)")
        self.fields["description_ar"].label = _("Description (Arabic)")
        self.fields["price"].label = _("Price (₪)")
        self.fields["image"].required = False
        self.fields["name_en"].required = False
        self.fields["name_ar"].required = False

    def clean(self) -> dict:
        cleaned_data = super().clean()
        name_en = (cleaned_data.get("name_en") or "").strip()
        name_ar = (cleaned_data.get("name_ar") or "").strip()

        if not name_en and not name_ar:
            raise forms.ValidationError(
                _("Please enter the item name in at least one language."),
            )

        cleaned_data["name_en"] = name_en or name_ar
        cleaned_data["name_ar"] = name_ar or name_en
        return cleaned_data

    def save(self, commit=True):
        item = super().save(commit=False)
        if commit:
            item.save()
            self.save_m2m()
        return item


class ReviewReplyForm(forms.ModelForm):
    """Post an owner reply beneath a customer review."""

    class Meta:
        model = CommentReply
        fields = ("reply_text",)
        widgets = {
            "reply_text": forms.TextInput(
                attrs={
                    "class": "rd-reply-input",
                    "placeholder": _("Reply to this review…"),
                },
            ),
        }


def get_or_create_default_menu_category(restaurant: Restaurant) -> MenuCategory:
    """Return the first menu category for a restaurant, creating one if needed."""
    category = restaurant.categories.order_by("order", "name_en").first()
    if category:
        return category
    return MenuCategory.objects.create(
        restaurant=restaurant,
        name_en="Main Dishes",
        name_ar="الأطباق الرئيسية",
        order=0,
    )
