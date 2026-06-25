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
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


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
        fields = ["full_name", "email", "role"]

    def clean_role(self) -> str:
        role = self.cleaned_data.get("role")
        if role == CustomUser.Role.ADMIN:
            raise forms.ValidationError(
                _("Admin role cannot be assigned during registration.")
            )
        return role

    def save(self, commit: bool = True) -> CustomUser:
        user = super().save(commit=False)
        parts = self.cleaned_data.get("full_name", "").strip().split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        user.role = self.cleaned_data.get("role", CustomUser.Role.USER)
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

        if user and selected_role and user.role != selected_role:
            raise forms.ValidationError(
                _("This account does not match the selected role."),
                code="role_mismatch",
            )
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Profile-edit form.

    Presents a single ``full_name`` field for simplicity, then writes
    first_name / last_name back to the model on save — consistent with
    the registration experience.

    Email and role changes require separate, admin-gated flows.

    Template context key: ``form``
    Fields rendered: full_name
    """

    full_name = forms.CharField(
        label=_("full name"),
        max_length=301,
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )

    class Meta:
        model = CustomUser
        fields: list = []  # All output comes from the custom full_name field.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["full_name"].initial = self.instance.full_name

    def save(self, commit: bool = True) -> CustomUser:
        user = super().save(commit=False)
        parts = self.cleaned_data.get("full_name", "").strip().split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        if commit:
            user.save(update_fields=["first_name", "last_name"])
        return user
