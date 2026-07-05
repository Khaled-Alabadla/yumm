"""Template tags for restaurant dashboard templates."""

from django import template
from django.utils import translation
from django.utils.translation import gettext as _

from restaurants.constants import (
    JPEG_MAGIC,
    TAG_NAME_AR,
    get_dish_image_url,
    get_restaurant_cover_url,
)
from restaurants.utils import is_open_now
register = template.Library()


@register.inclusion_tag("restaurants/dashboard/_stars.html")
def star_rating(rating):
    rating = int(rating or 0)
    return {
        "full_stars": range(rating),
        "empty_stars": range(5 - rating),
        "rating": rating,
    }


@register.filter
def localized_name(obj):
    if translation.get_language() == "ar":
        return obj.name_ar or obj.name_en
    return obj.name_en or obj.name_ar


@register.filter
def localized_description(obj):
    if translation.get_language() == "ar":
        return obj.description_ar or obj.description_en
    return obj.description_en or obj.description_ar


@register.filter
def localized_address(restaurant):
    if translation.get_language() == "ar":
        return restaurant.address_ar or restaurant.address_en
    return restaurant.address_en or restaurant.address_ar


@register.filter
def restaurant_is_open(restaurant):
    return is_open_now(restaurant)


@register.filter
def localized_category(category):
    if not category:
        return ""
    if translation.get_language() == "ar":
        return category.name_ar or category.name_en
    return category.name_en or category.name_ar


@register.filter
def localized_tag(tag):
    if translation.get_language() == "ar":
        if tag.name_ar and tag.name_ar != tag.name_en:
            return tag.name_ar
        return TAG_NAME_AR.get(tag.name_en) or _(tag.name_en)
    return tag.name_en or tag.name_ar


@register.filter
def menu_item_image(item):
    """Owner upload wins; otherwise use authentic local dish photo."""
    if item.image and item.image.name:
        try:
            if item.image.storage.exists(item.image.name):
                return item.image.url
        except OSError:
            pass
    return get_dish_image_url(item.name_en)


@register.filter
def menu_item_has_upload(item):
    return bool(item.image)


@register.filter
def price_range_symbols(restaurant):
    level = restaurant.price_range or 2
    return "₪" * level


@register.inclusion_tag("restaurants/_price_range.html")
def price_range_badge(restaurant, variant="tag"):
    level = restaurant.price_range or 2
    labels = {
        1: _("Budget"),
        2: _("Moderate"),
        3: _("Expensive"),
    }
    return {
        "label": labels.get(level, labels[2]),
        "symbols": "₪" * level,
        "variant": variant,
    }


def _is_valid_uploaded_image(image_field) -> bool:
    if not image_field or not image_field.name:
        return False
    try:
        if not image_field.storage.exists(image_field.name):
            return False
        with image_field.open("rb") as handle:
            return handle.read(3) == JPEG_MAGIC
    except OSError:
        return False


@register.filter
def restaurant_cover(restaurant):
    """Return cover image URL — unique local restaurant photo per listing."""
    primary = restaurant.primary_image
    if primary and primary.image and _is_valid_uploaded_image(primary.image):
        return primary.image.url
    cat_name = restaurant.category.name_en if restaurant.category else ""
    return get_restaurant_cover_url(restaurant.name_en or "", cat_name)


@register.inclusion_tag("partials/_landing_stars.html")
def landing_stars(rating):
    full = max(0, min(5, round(float(rating or 0))))
    return {
        "full_stars": range(full),
        "empty_stars": range(5 - full),
        "rating": rating,
    }


@register.inclusion_tag("restaurants/_stars.html")
def public_stars(rating, size="sm"):
    full = max(0, min(5, round(float(rating or 0))))
    return {
        "full_stars": range(full),
        "half_star": 0,
        "empty_stars": range(5 - full),
        "rating": full,
        "size": size,
    }


@register.filter
def city_label(restaurant):
    return restaurant.get_city_display()


@register.filter
def timesince_short(value):
    from django.utils.timesince import timesince

    if not value:
        return ""
    return timesince(value, depth=1)


@register.filter
def get_item(mapping, key):
    if mapping is None:
        return None
    return mapping.get(key)


@register.filter
def user_display_name(user):
    if not user:
        return ""
    name = f"{user.first_name} {user.last_name}".strip()
    return name or user.email.split("@")[0]
