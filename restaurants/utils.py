"""Dashboard analytics helpers."""

import re
from datetime import datetime, time, timedelta

from django.db.models import Avg, Count
from django.utils import timezone


def get_review_stats(restaurant) -> dict:
    """
    Return aggregate review metrics and 30-day growth deltas for the dashboard.
    """
    now = timezone.now()
    last_30 = now - timedelta(days=30)
    prev_30_start = now - timedelta(days=60)

    visible = restaurant.reviews.filter(is_visible=True)
    totals = visible.aggregate(
        count=Count("id"),
        avg=Avg("rating"),
    )

    last_period = visible.filter(created_at__gte=last_30)
    prev_period = visible.filter(
        created_at__gte=prev_30_start,
        created_at__lt=last_30,
    )

    last_count = last_period.count()
    prev_count = prev_period.count()

    if prev_count:
        review_growth_pct = round((last_count - prev_count) / prev_count * 100)
    elif last_count:
        review_growth_pct = 100
    else:
        review_growth_pct = None

    last_avg = last_period.aggregate(avg=Avg("rating"))["avg"]
    prev_avg = prev_period.aggregate(avg=Avg("rating"))["avg"]

    if last_avg is not None and prev_avg is not None:
        rating_growth = round(last_avg - prev_avg, 1)
    else:
        rating_growth = None

    avg_rating = totals["avg"]
    return {
        "total_reviews": totals["count"] or 0,
        "avg_rating": round(avg_rating, 1) if avg_rating is not None else None,
        "review_growth_pct": review_growth_pct,
        "rating_growth": rating_growth,
    }


def parse_working_hours(working_hours: str) -> tuple[str, str]:
    """Split a stored working-hours string into opening and closing parts."""
    if not working_hours:
        return "", ""
    for separator in (" - ", " – ", "-"):
        if separator in working_hours:
            parts = working_hours.split(separator, 1)
            return parts[0].strip(), parts[1].strip()
    return working_hours.strip(), ""


def normalize_time_for_input(value: str) -> str:
    """Convert stored or legacy time strings to ``HH:MM`` for HTML time inputs."""
    value = (value or "").strip()
    if not value:
        return ""

    if re.fullmatch(r"\d{1,2}:\d{2}", value):
        hour, minute = value.split(":", 1)
        return f"{int(hour):02d}:{minute}"

    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M", "%I %p"):
        try:
            return datetime.strptime(value, fmt).strftime("%H:%M")
        except ValueError:
            continue

    return value


def parse_time_value(value: str) -> time | None:
    """Parse a time string into a ``datetime.time`` for form initial values."""
    normalized = normalize_time_for_input(value)
    if not normalized:
        return None
    try:
        return datetime.strptime(normalized, "%H:%M").time()
    except ValueError:
        return None


def format_working_hours(opening: str | time | None, closing: str | time | None) -> str:
    """Combine opening and closing times into a single stored string."""
    def _as_text(value: str | time | None) -> str:
        if value is None:
            return ""
        if isinstance(value, time):
            return value.strftime("%H:%M")
        return normalize_time_for_input(str(value))

    opening_text = _as_text(opening)
    closing_text = _as_text(closing)
    if opening_text and closing_text:
        return f"{opening_text} - {closing_text}"
    return opening_text or closing_text


def is_open_now(restaurant) -> bool:
    """
    Return whether the restaurant is open right now based on working hours.

    Falls back to the manual ``is_open`` flag when hours are not configured.
    """
    hours = restaurant.working_hours_en or restaurant.working_hours_ar or ""
    opening_str, closing_str = parse_working_hours(hours)
    opening = parse_time_value(opening_str)
    closing = parse_time_value(closing_str)

    if not opening or not closing:
        return bool(restaurant.is_open)

    now = timezone.localtime().time()
    if opening <= closing:
        return opening <= now <= closing
    return now >= opening or now <= closing
