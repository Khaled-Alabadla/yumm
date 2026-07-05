"""Restaurants app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestaurantsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restaurants"
    verbose_name = _("Restaurants")

    def ready(self) -> None:
        import restaurants.signals  # noqa: F401
