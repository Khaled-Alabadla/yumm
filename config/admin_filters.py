"""Admin list filters that work without MySQL time zone tables."""

from datetime import timedelta

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class RecentCreatedFilter(admin.SimpleListFilter):
    """
    Filter by created_at using direct range comparisons.

    Unlike DateFieldListFilter / date_hierarchy, this does not call MySQL
    CONVERT_TZ(), so it works when mysql.time_zone_name is empty (common on
    Windows MySQL installs).
    """

    title = _("created at")
    parameter_name = "created"

    def lookups(self, request, model_admin):
        return (
            ("today", _("Today")),
            ("7days", _("Past 7 days")),
            ("30days", _("Past 30 days")),
            ("year", _("Past year")),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        now = timezone.now()
        start = {
            "today": now.replace(hour=0, minute=0, second=0, microsecond=0),
            "7days": now - timedelta(days=7),
            "30days": now - timedelta(days=30),
            "year": now - timedelta(days=365),
        }.get(value)

        if start is None:
            return queryset
        return queryset.filter(created_at__gte=start)
