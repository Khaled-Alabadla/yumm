"""Shared wishlist helpers for views and template context."""

from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _

from restaurants.models import Restaurant
from restaurants.querysets import annotate_public_stats
from reviews.models import Wishlist


def _localized_name(restaurant) -> str:
    if translation.get_language() == "ar":
        return restaurant.name_ar or restaurant.name_en
    return restaurant.name_en or restaurant.name_ar


def _localized_category(category) -> str:
    if not category:
        return ""
    if translation.get_language() == "ar":
        return category.name_ar or category.name_en
    return category.name_en or category.name_ar


def get_wishlist_ids(user) -> set[int]:
    if not user.is_authenticated or user.is_owner_role:
        return set()
    return set(
        Wishlist.objects.filter(user=user).values_list("restaurant_id", flat=True)
    )


def get_wishlist_items(user) -> list[dict]:
    if not user.is_authenticated or user.is_owner_role:
        return []
    entries = (
        Wishlist.objects.filter(user=user, restaurant__status=Restaurant.Status.ACTIVE)
        .select_related("restaurant", "restaurant__category")
        .order_by("-created_at")
    )
    restaurant_ids = [entry.restaurant_id for entry in entries]
    stats = {
        row.pk: row
        for row in annotate_public_stats(
            Restaurant.objects.filter(pk__in=restaurant_ids)
        )
    }
    items = []
    for entry in entries:
        restaurant = stats.get(entry.restaurant_id, entry.restaurant)
        items.append(
            {
                "id": restaurant.pk,
                "name": _localized_name(restaurant),
                "cuisine": _localized_category(restaurant.category),
                "city": restaurant.get_city_display(),
                "rating": f"{restaurant.avg_rating:.1f}" if restaurant.avg_rating else "",
                "url": reverse("restaurants:detail", args=[restaurant.pk]),
            }
        )
    return items


def get_wishlist_i18n() -> dict:
    return {
        "wishlistEmpty": _("Nothing saved yet"),
        "wishlistHint": _("Tap ♥ on a restaurant to save it"),
        "savedOne": _("1 restaurant saved"),
        "savedMany": _("restaurants saved"),
        "added": _("Added to wishlist"),
        "removed": _("Removed from wishlist"),
        "loginRequired": _("Please log in to save restaurants to your wishlist"),
    }
