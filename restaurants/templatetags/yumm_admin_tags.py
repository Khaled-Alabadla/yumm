"""Template tags for the Yumm admin dashboard."""

from django import template

from config.dashboard import get_platform_stats

register = template.Library()


@register.simple_tag
def yumm_platform_stats() -> dict:
    return get_platform_stats()
