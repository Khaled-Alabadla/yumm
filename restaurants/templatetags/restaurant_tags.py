"""Template tags for restaurant dashboard templates."""

from django import template
from django.utils import translation

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
