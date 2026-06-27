"""Shared dashboard metrics for the Yumm admin panel."""

from django.contrib.auth import get_user_model
from django.db.models import Avg


def get_platform_stats() -> dict:
    from restaurants.models import Restaurant
    from reviews.models import Review

    User = get_user_model()
    rating_agg = Review.objects.aggregate(avg=Avg("rating"))
    avg_rating = rating_agg["avg"]

    return {
        "total_users": User.objects.count(),
        "active_restaurants": Restaurant.objects.filter(
            status=Restaurant.Status.ACTIVE
        ).count(),
        "pending_restaurants": Restaurant.objects.filter(
            status=Restaurant.Status.PENDING
        ).count(),
        "total_reviews": Review.objects.count(),
        "average_rating": round(avg_rating, 1) if avg_rating is not None else None,
    }
