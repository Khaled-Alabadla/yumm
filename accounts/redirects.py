"""Role-based redirect helpers for authenticated users."""

from django.shortcuts import redirect


def owner_home_url_name(user) -> str:
    """Return the URL name for an owner's primary destination."""
    if user.is_pending_owner:
        return "accounts:pending"
    return "restaurants:dashboard"


def redirect_owner_home(user):
    """Redirect a restaurant owner to their dashboard (or pending page)."""
    return redirect(owner_home_url_name(user))
