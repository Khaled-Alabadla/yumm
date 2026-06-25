"""Role-based access control decorators and class-based view mixins.

All responses are template-friendly: unauthenticated requests are
redirected to the login page; wrong-role requests raise PermissionDenied
so Django renders the standard 403 page (customisable via 403.html).

Function decorators — use with any function-based view:
    @login_required
    @admin_required
    def my_admin_view(request): ...

    @login_required
    @owner_required
    def my_owner_view(request): ...

CBV mixins — place before the primary view class in the MRO:
    class MyView(AdminRequiredMixin, View): ...
    class MyView(OwnerRequiredMixin, TemplateView): ...
    class MyView(AdminOrOwnerRequiredMixin, UpdateView): ...
"""

import functools

from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


# ---------------------------------------------------------------------------
# Function-based view decorators
# ---------------------------------------------------------------------------

def admin_required(view_func):
    """Restrict a FBV to users with role == 'admin'."""

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not request.user.is_admin_role:
            raise PermissionDenied(_("Admin access required."))
        return view_func(request, *args, **kwargs)

    return wrapper


def owner_required(view_func):
    """Restrict a FBV to users with role == 'owner'."""

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not request.user.is_owner_role:
            raise PermissionDenied(_("Owner access required."))
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_or_owner_required(view_func):
    """Restrict a FBV to users with role == 'admin' or 'owner'."""

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not (request.user.is_admin_role or request.user.is_owner_role):
            raise PermissionDenied(_("Admin or Owner access required."))
        return view_func(request, *args, **kwargs)

    return wrapper


# ---------------------------------------------------------------------------
# Class-based view mixins
# ---------------------------------------------------------------------------

class AdminRequiredMixin(DjangoLoginRequiredMixin):
    """
    Allow only admin-role users.

    Unauthenticated requests → redirect to settings.LOGIN_URL (via parent).
    Authenticated non-admin  → PermissionDenied (HTTP 403).
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_admin_role:
            raise PermissionDenied(_("Admin access required."))
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(DjangoLoginRequiredMixin):
    """
    Allow only owner-role users.

    Unauthenticated requests → redirect to settings.LOGIN_URL (via parent).
    Authenticated non-owner  → PermissionDenied (HTTP 403).
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_owner_role:
            raise PermissionDenied(_("Owner access required."))
        return super().dispatch(request, *args, **kwargs)


class AdminOrOwnerRequiredMixin(DjangoLoginRequiredMixin):
    """
    Allow admin-role or owner-role users.

    Unauthenticated requests           → redirect to settings.LOGIN_URL.
    Authenticated plain-user requests  → PermissionDenied (HTTP 403).
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.is_admin_role or request.user.is_owner_role):
            raise PermissionDenied(_("Admin or Owner access required."))
        return super().dispatch(request, *args, **kwargs)
