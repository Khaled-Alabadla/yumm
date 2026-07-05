"""Template context processors for the accounts app."""

from django.utils.translation import gettext as _

from .wishlist_utils import get_wishlist_i18n, get_wishlist_ids, get_wishlist_items

_DESKTOP = {
    "active": "text-[#B5451B] bg-[#B5451B]/10 dark:bg-[#B5451B]/15 font-semibold",
    "inactive": "text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-[#2A2A2A]",
}

_MOBILE = {
    "active": "text-[#B5451B] bg-[#B5451B]/10 dark:bg-[#B5451B]/15 font-semibold",
    "inactive": "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#2A2A2A]",
}

_AUTH = {
    "active": "text-[#B5451B] bg-[#B5451B]/10 dark:bg-[#B5451B]/15 font-semibold",
    "inactive": "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#2A2A2A]",
}

_REGISTER = {
    "active": "ring-2 ring-[#B5451B]/40",
    "inactive": "",
}

_NAV_SECTIONS = ("home", "restaurants", "ai", "login", "register", "profile", "dashboard")


def _is_active(request, section: str) -> bool:
    path = request.path.rstrip("/") or "/"
    match = getattr(request, "resolver_match", None)
    name = match.url_name if match else None
    namespace = match.namespace if match else None

    if section == "home":
        return path == "/" or (namespace == "accounts" and name == "index" and path == "/accounts")
    if section == "restaurants":
        return path == "/restaurants" or path.startswith("/restaurants/")
    if section == "ai":
        return path == "/ai" or path.startswith("/ai/")
    if section == "login":
        return namespace == "accounts" and name == "login"
    if section == "register":
        return namespace == "accounts" and name == "register"
    if section == "profile":
        return namespace == "accounts" and name == "profile"
    if section == "dashboard":
        return namespace == "restaurants" and name and name.startswith("dashboard")
    return False


def _nav_state(request):
    nav = {}
    for section in _NAV_SECTIONS:
        active = _is_active(request, section)
        state = "active" if active else "inactive"
        nav[section] = {
            "active": active,
            "desktop": _DESKTOP[state],
            "mobile": _MOBILE[state],
            "auth": _AUTH[state],
            "register": _REGISTER[state],
        }
    return nav


def navbar(request):
    return {"nav": _nav_state(request)}


def wishlist(request):
    user = request.user
    items = get_wishlist_items(user)
    return {
        "wishlist_ids": get_wishlist_ids(user),
        "wishlist_items": items,
        "wishlist_count": len(items),
        "wishlist_i18n": get_wishlist_i18n(),
    }
