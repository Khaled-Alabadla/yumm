"""Middleware that keeps restaurant owners on their dashboard."""

from django.shortcuts import redirect

from .redirects import owner_home_url_name


class OwnerDashboardRedirectMiddleware:
    """
    Approved owners may only access the owner dashboard (plus logout/i18n/static).
    Pending owners are limited to the pending-approval page.
    """

    _ALWAYS_ALLOWED = (
        "/static/",
        "/media/",
        "/i18n/",
    )
    _APPROVED_OWNER_ALLOWED = (
        "/dashboard/",
        "/accounts/logout",
    )
    _PENDING_OWNER_ALLOWED = (
        "/accounts/pending",
        "/accounts/logout",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated and user.is_owner_role:
            path = request.path

            if any(path.startswith(prefix) for prefix in self._ALWAYS_ALLOWED):
                return self.get_response(request)

            allowed = (
                self._PENDING_OWNER_ALLOWED
                if user.is_pending_owner
                else self._APPROVED_OWNER_ALLOWED
            )
            if not any(path.startswith(prefix) for prefix in allowed):
                return redirect(owner_home_url_name(user))

        return self.get_response(request)
