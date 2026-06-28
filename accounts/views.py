"""Authentication views for the accounts app.

All views are class-based and template-driven.
No JSON/DRF responses are used — context is passed to templates.

Views:
    RegisterView    GET+POST /accounts/register/
    LoginView       GET+POST /accounts/login/
    LogoutView      POST     /accounts/logout/
    ProfileView     GET+POST /accounts/profile/
    DemoLoginView   POST     /accounts/demo-login/   (DEBUG only)

Template contract (context keys available in every view's template):
    form          — the bound/unbound form instance
    page_title    — translated string for <title> / <h1>
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import CustomUser

# Shared by RegisterView and LoginView — keeps the toggle choices in one place.
_ROLE_CHOICES = [
    (CustomUser.Role.USER, _("Regular User")),
    (CustomUser.Role.OWNER, _("Restaurant Owner")),
]


class RegisterView(CreateView):
    """
    GET  — render the registration form.
    POST — validate, create user, redirect to login with a success message.

    Authenticated users are bounced directly to their profile.
    Template: accounts/register.html
    Context:  form, page_title
    """

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def get_success_url(self):
        if self.object.role == CustomUser.Role.OWNER:
            return reverse_lazy("accounts:pending")
        return reverse_lazy("accounts:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("accounts:profile"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            _("Registration successful. Please log in."),
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            _("Registration failed. Please correct the errors below."),
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Create Account")
        context["role_choices"] = _ROLE_CHOICES
        return context


class LoginView(BaseLoginView):
    """
    GET  — render the login form.
    POST — authenticate, enforce role match, open session, redirect.

    Wraps Django's built-in LoginView so ?next=, CSRF, and session
    management are all handled by the framework.
    Template: accounts/login.html
    Context:  form, page_title, role_choices, demo_enabled
    """

    form_class = UserLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, _("Login successful."))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Invalid credentials."))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Sign In")
        context["role_choices"] = _ROLE_CHOICES
        context["demo_enabled"] = settings.DEBUG
        return context


class LogoutView(BaseLogoutView):
    """
    POST /accounts/logout/

    Destroys the session and redirects to the login page.
    GET requests are rejected by Django's BaseLogoutView (CSRF safety).
    Template: none — pure redirect.
    """

    next_page = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("Logged out successfully."))
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    GET  — render the profile form pre-filled with current user data.
    POST — validate, save name, redirect back to profile.

    LoginRequiredMixin redirects unauthenticated users to settings.LOGIN_URL.
    Template: accounts/profile.html
    Context:  form, page_title, user (the authenticated user object)
    """

    model = CustomUser
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None) -> CustomUser:
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Profile updated successfully."))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            _("Profile update failed. Please correct the errors below."),
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("My Profile")
        return context


class DemoLoginView(View):
    """
    POST /accounts/demo-login/

    Quick demo access — matches the "User / Owner / Admin" buttons in
    the login design.  Only available when settings.DEBUG is True.

    Expected POST field:  role = "user" | "owner" | "admin"

    On first call for each role, a demo account is created automatically.
    Passwords are set but never need to be known by a human tester.

    Template: none — redirects to profile on success, login on error.
    """

    # Demo account definitions.  Credentials are intentionally weak
    # because these accounts must only exist in a DEBUG environment.
    _DEMO_ACCOUNTS: dict[str, dict] = {
        CustomUser.Role.USER: {
            "email": "demo.user@yumm.ps",
            "password": "DemoUser@Yumm2024",
            "first_name": "Demo",
            "last_name": "User",
        },
        CustomUser.Role.OWNER: {
            "email": "demo.owner@yumm.ps",
            "password": "DemoOwner@Yumm2024",
            "first_name": "Demo",
            "last_name": "Owner",
        },
        CustomUser.Role.ADMIN: {
            "email": "demo.admin@yumm.ps",
            "password": "DemoAdmin@Yumm2024",
            "first_name": "Demo",
            "last_name": "Admin",
        },
    }

    def dispatch(self, request, *args, **kwargs):
        if not settings.DEBUG:
            return HttpResponseForbidden(
                str(_("Demo login is only available in DEBUG mode."))
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        role = request.POST.get("role", "").strip()

        if role not in self._DEMO_ACCOUNTS:
            messages.error(request, _("Invalid demo role."))
            return redirect(reverse_lazy("accounts:login"))

        credentials = self._DEMO_ACCOUNTS[role]
        user = self._get_or_create_demo_user(role, credentials)

        login(request, user)
        messages.info(
            request,
            _("Logged in as demo %(role)s account.") % {"role": role},
        )
        return redirect(reverse_lazy("accounts:profile"))

    @staticmethod
    def _get_or_create_demo_user(role: str, credentials: dict) -> CustomUser:
        """Return the demo user for the given role, creating it if absent."""
        user, created = CustomUser.objects.get_or_create(
            email=credentials["email"],
            defaults={
                "first_name": credentials["first_name"],
                "last_name": credentials["last_name"],
                "role": role,
                "is_active": True,
                "is_staff": role == CustomUser.Role.ADMIN,
                "is_superuser": role == CustomUser.Role.ADMIN,
            },
        )
        if created:
            user.set_password(credentials["password"])
            user.save(update_fields=["password"])
        return user

class PendingView(TemplateView):
    template_name = "accounts/pending.html"
