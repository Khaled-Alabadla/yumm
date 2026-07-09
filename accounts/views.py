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
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.translation import gettext, gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from restaurants.models import Restaurant
from restaurants.querysets import (
    annotate_public_stats,
    get_landing_review_highlights,
    get_landing_stats,
    get_map_restaurants,
    get_top_rated_restaurants,
)

from .forms import ContactForm, UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import CustomUser
from .redirects import redirect_owner_home
# Shared by RegisterView and LoginView — keeps the toggle choices in one place.
_ROLE_CHOICES = [
    (CustomUser.Role.USER, _("Regular User")),
    (CustomUser.Role.OWNER, _("Restaurant Owner")),
]


def get_cta_subtitle(user_count: int) -> str:
    if user_count == 1:
        return gettext(
            "Join one food lover discovering Palestine's best restaurants every day."
        )
    return gettext(
        "Join %(count)s food lovers discovering Palestine's best restaurants every day."
    ) % {"count": user_count}


def _localized_restaurant_name(restaurant) -> str:
    if translation.get_language() == "ar":
        return restaurant.name_ar or restaurant.name_en
    return restaurant.name_en or restaurant.name_ar


def _localized_category_name(category) -> str:
    if not category:
        return ""
    if translation.get_language() == "ar":
        return category.name_ar or category.name_en
    return category.name_en or category.name_ar


def _landing_map_markers() -> list[dict]:
    qs = annotate_public_stats(get_map_restaurants())
    markers = []
    for restaurant in qs:
        if restaurant.latitude is None or restaurant.longitude is None:
            continue
        parts = []
        if restaurant.category:
            parts.append(_localized_category_name(restaurant.category))
        parts.append(restaurant.get_city_display())
        if restaurant.avg_rating:
            parts.append(f"★ {restaurant.avg_rating:.1f}")
        markers.append(
            {
                "id": restaurant.pk,
                "name": _localized_restaurant_name(restaurant),
                "lat": float(restaurant.latitude),
                "lng": float(restaurant.longitude),
                "url": reverse("restaurants:detail", args=[restaurant.pk]),
                "desc": " · ".join(parts),
                "city": restaurant.get_city_display(),
            }
        )
    return markers


def index(request):
    if request.user.is_authenticated and request.user.is_owner_role:
        return redirect_owner_home(request.user)

    map_markers = _landing_map_markers()
    top_restaurants = list(get_top_rated_restaurants(limit=3))
    map_featured = [
        marker
        for marker in map_markers
        if marker["id"] in {r.pk for r in top_restaurants}
    ][:3]
    if len(map_featured) < 3:
        seen = {m["id"] for m in map_featured}
        for marker in map_markers:
            if marker["id"] not in seen:
                map_featured.append(marker)
                seen.add(marker["id"])
            if len(map_featured) >= 3:
                break

    stats = get_landing_stats()
    return render(
        request,
        "index.html",
        {
            "stats": stats,
            "cta_subtitle": get_cta_subtitle(stats["users"]),
            "top_restaurants": top_restaurants,
            "review_highlights": get_landing_review_highlights(),
            "map_restaurants": map_markers,
            "map_featured": map_featured,
        },
    )

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
        return reverse_lazy("accounts:check_email")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_owner_role:
                return redirect_owner_home(request.user)
            return redirect(reverse_lazy("index"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.role == CustomUser.Role.USER:
            from .emails import send_user_verification_email

            send_user_verification_email(self.object, self.request)
            messages.success(
                self.request,
                _("Account created. Please confirm your email to continue."),
            )
        else:
            messages.success(
                self.request,
                _("Registration successful. Your request is pending approval."),
            )
        return response

    def form_invalid(self, form):
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors()[0])
        elif form.errors:
            messages.error(
                self.request,
                _("Registration failed. Please correct the errors below."),
            )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Create Account")
        context["role_choices"] = _ROLE_CHOICES
        if self.request.method == "POST":
            context["selected_role"] = self.request.POST.get(
                "role", CustomUser.Role.USER
            )
        else:
            context["selected_role"] = CustomUser.Role.USER
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

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.is_owner_role:
            return reverse_lazy("restaurants:dashboard")

        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        return super().get_success_url()

    def form_valid(self, form):
        messages.success(self.request, _("Login successful."))
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors()[0])
        else:
            messages.error(self.request, _("Invalid credentials."))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Sign In")
        context["role_choices"] = _ROLE_CHOICES
        context["demo_enabled"] = settings.DEBUG
        if self.request.method == "POST":
            context["selected_role"] = self.request.POST.get(
                "role", CustomUser.Role.USER
            )
        else:
            context["selected_role"] = CustomUser.Role.USER
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
        password_changed = bool(form.cleaned_data.get("new_password1"))
        response = super().form_valid(form)
        if password_changed:
            update_session_auth_hash(self.request, form.instance)
            messages.success(
                self.request,
                _("Profile and password updated successfully."),
            )
        else:
            messages.success(self.request, _("Profile updated successfully."))
        return response

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
        if role == CustomUser.Role.OWNER:
            return redirect(reverse_lazy("restaurants:dashboard"))
        if role == CustomUser.Role.ADMIN:
            return redirect(reverse_lazy("admin:index"))
        return redirect(reverse_lazy("index"))

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
                "is_approved": True,
                "is_staff": role == CustomUser.Role.ADMIN,
                "is_superuser": role == CustomUser.Role.ADMIN,
            },
        )
        if created:
            user.set_password(credentials["password"])
            user.save(update_fields=["password"])
        return user
def about(request):
    return render(request, "pages/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                _("Message sent! We'll get back to you within 24 hours."),
            )
            return redirect("contact")
        messages.error(request, _("Please fix the errors below."))
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})


def privacy(request):
    return render(
        request,
        "pages/privacy.html",
        {"last_updated": _("July 2026")},
    )


def terms(request):
    return render(
        request,
        "pages/terms.html",
        {"last_updated": _("July 2026")},
    )

class PendingView(TemplateView):
    template_name = "accounts/pending.html"


class CheckEmailView(TemplateView):
    """Shown after regular-user registration — ask them to confirm email."""

    template_name = "accounts/check_email.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("index"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Check your email")
        return context


class VerifyEmailView(View):
    """Activate a regular user account from the emailed confirmation link."""

    def get(self, request, uidb64, token):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        user = None
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if (
            user is not None
            and user.role == CustomUser.Role.USER
            and default_token_generator.check_token(user, token)
        ):
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
            messages.success(
                request,
                _("Email confirmed successfully. You may now sign in."),
            )
            return redirect("accounts:login")

        messages.error(
            request,
            _("This confirmation link is invalid or has expired."),
        )
        return redirect("accounts:login")
