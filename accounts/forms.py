"""Django forms for the accounts app.

These forms own all validation logic so views stay thin.
Your frontend colleague binds them to templates via the context key "form".

Forms:
    UserRegistrationForm  — sign-up (extends UserCreationForm)
    UserLoginForm         — sign-in  (extends AuthenticationForm, adds role toggle)
    UserProfileForm       — profile edit (name fields only)
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

phone_validator = RegexValidator(
    regex=r"^[\d\s+\-()]{7,20}$",
    message=_("Enter a valid phone number."),
)


def _clean_phone_field(form, cleaned_data: dict, *, required: bool = False) -> dict:
    phone = (cleaned_data.get("phone") or "").strip()
    if not phone:
        if required:
            form.add_error(
                "phone",
                _("Phone number is required for restaurant owners."),
            )
        else:
            cleaned_data["phone"] = ""
        return cleaned_data

    try:
        phone_validator(phone)
    except ValidationError as exc:
        form.add_error("phone", exc.messages[0])
    else:
        cleaned_data["phone"] = phone

    return cleaned_data


def _style_phone_field(form) -> None:
    if "phone" not in form.fields:
        return
    form.fields["phone"].required = False
    form.fields["phone"].widget.attrs.update(
        {
            "autocomplete": "tel",
            "placeholder": "+970 59 000 0000",
            "class": "w-full rounded-xl px-4 py-3 text-sm outline-none transition-colors",
        }
    )


class UserRegistrationForm(UserCreationForm):
    """
    Sign-up form.

    Uses a single ``full_name`` field that is split into first_name /
    last_name on save, matching the design's single "Full Name" input.

    Role is collected as a toggle ("Regular User" / "Restaurant Owner").
    Admin role cannot be self-assigned.

    Template context key: ``form``
    Fields rendered: full_name, email, role, password1, password2
    """

    full_name = forms.CharField(
        label=_("full name"),
        max_length=301,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "name",
                "placeholder": _("Ahmad Al-Khalidi"),
            }
        ),
    )
    role = forms.ChoiceField(
        label=_("account type"),
        choices=[
            (CustomUser.Role.USER,  _("Regular User")),
            (CustomUser.Role.OWNER, _("Restaurant Owner")),
        ],
        initial=CustomUser.Role.USER,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = CustomUser
        # password1 / password2 come from UserCreationForm — not listed here.
        fields = ["full_name", "email", "role", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_phone_field(self)

    def clean_role(self) -> str:
        role = self.cleaned_data.get("role")
        if role == CustomUser.Role.ADMIN:
            raise forms.ValidationError(
                _("Admin role cannot be assigned during registration.")
            )
        return role

    def clean(self) -> dict:
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        return _clean_phone_field(
            self,
            cleaned_data,
            required=role == CustomUser.Role.OWNER,
        )

    def save(self, commit: bool = True) -> CustomUser:
        user = super().save(commit=False)
        parts = self.cleaned_data.get("full_name", "").strip().split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        user.role = self.cleaned_data.get("role", CustomUser.Role.USER)
        user.phone = self.cleaned_data.get("phone", "")
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Login form.

    Extends Django's AuthenticationForm — all session handling, CSRF,
    and password checking is provided by the framework.

    Adds an optional ``role`` toggle so the backend can validate that
    the authenticated user actually belongs to the selected role
    (matches the "Regular User" / "Restaurant Owner" toggle in the design).

    If ``role`` is left blank the check is skipped (safe fallback).

    Template context key: ``form``
    Fields rendered: username (auto-labelled "email address"), password, role
    """

    role = forms.ChoiceField(
        label=_("account type"),
        choices=[
            ("",                    _("Any")),
            (CustomUser.Role.USER,  _("Regular User")),
            (CustomUser.Role.OWNER, _("Restaurant Owner")),
        ],
        required=False,
        initial=CustomUser.Role.USER,
        widget=forms.RadioSelect,
    )

    def clean(self) -> dict:
        """Run parent auth then enforce role match when a role is selected."""
        cleaned_data = super().clean()
        user = self.get_user()
        selected_role = cleaned_data.get("role", "")

        if user and user.is_owner_role and not user.is_approved:
            raise forms.ValidationError(
                _(
                    "Your restaurant owner account is pending admin approval. "
                    "You will be able to sign in once approved."
                ),
                code="pending_owner",
            )

        if user and selected_role and user.role != selected_role:
            raise forms.ValidationError(
                _("This account does not match the selected role."),
                code="role_mismatch",
            )
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Profile-edit form.

    Editable: full_name, phone, and optional password change.
    Email, role, and approval status are read-only in the template.
    """

    full_name = forms.CharField(
        label=_("full name"),
        max_length=301,
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )
    current_password = forms.CharField(
        label=_("current password"),
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": _("Required to change password"),
            }
        ),
    )
    new_password1 = forms.CharField(
        label=_("new password"),
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": _("Leave blank to keep current password"),
            }
        ),
    )
    new_password2 = forms.CharField(
        label=_("confirm new password"),
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": _("Repeat new password"),
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["phone", "city", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["full_name"].initial = self.instance.full_name
        _style_phone_field(self)

        from restaurants.models import Restaurant

        field_class = (
            "w-full rounded-xl px-4 py-3 text-sm outline-none transition-colors"
        )
        self.fields["city"] = forms.ChoiceField(
            label=_("city"),
            choices=[("", _("Select a city"))] + list(Restaurant.City.choices),
            required=False,
            widget=forms.Select(attrs={"class": field_class}),
        )
        if self.instance.pk and self.instance.city:
            self.fields["city"].initial = self.instance.city

        self.fields["address"].label = _("address")
        self.fields["address"].required = False
        self.fields["address"].widget = forms.TextInput(
            attrs={
                "autocomplete": "street-address",
                "placeholder": _("Street, building, area…"),
                "class": field_class,
            }
        )

    def clean(self) -> dict:
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        changing_password = any([current_password, new_password1, new_password2])

        if changing_password:
            if not current_password:
                self.add_error(
                    "current_password",
                    _("Enter your current password to set a new one."),
                )
            elif not self.instance.check_password(current_password):
                self.add_error(
                    "current_password",
                    _("Your current password is incorrect."),
                )

            if not new_password1:
                self.add_error(
                    "new_password1",
                    _("Enter a new password or leave all password fields blank."),
                )
            elif new_password1 != new_password2:
                self.add_error("new_password2", _("The two password fields didn't match."))
            else:
                from django.contrib.auth.password_validation import validate_password

                validate_password(new_password1, self.instance)

        cleaned_data = _clean_phone_field(
            self,
            cleaned_data,
            required=self.instance.is_owner_role,
        )

        if self.instance.is_owner_role:
            city = (cleaned_data.get("city") or "").strip()
            address = (cleaned_data.get("address") or "").strip()
            if not city:
                self.add_error(
                    "city",
                    _("City is required for restaurant owners."),
                )
            if not address:
                self.add_error(
                    "address",
                    _("Address is required for restaurant owners."),
                )
            cleaned_data["city"] = city
            cleaned_data["address"] = address

        return cleaned_data

    def save(self, commit: bool = True) -> CustomUser:
        user = super().save(commit=False)
        parts = self.cleaned_data.get("full_name", "").strip().split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        user.phone = self.cleaned_data.get("phone", "")

        new_password = self.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        error_messages={'required': 'Please enter your name.'}
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Please enter your email.',
            'invalid': 'Enter a valid email address.'
        }
    )
    subject = forms.ChoiceField(choices=[
        ('Restaurant Partnership', 'Restaurant Partnership'),
        ('Technical Support',      'Technical Support'),
        ('Media & Press',          'Media & Press'),
        ('General Inquiry',        'General Inquiry'),
    ])
    message = forms.CharField(
        widget=forms.Textarea,
        min_length=10,
        max_length=1000,
        error_messages={
            'required': 'Please enter a message.',
            'min_length': 'Message must be at least 10 characters.'
        }
    )
