"""Query helpers for public restaurant pages."""

from django.db.models import Avg, Count, F, Prefetch, Q, QuerySet

from reviews.models import Review

from accounts.models import CustomUser

from .models import MenuCategory, MenuItem, Restaurant, RestaurantCategory

# Cities shown as quick-filter chips on the list page.
FEATURED_CITY_CODES = (
    Restaurant.City.RAMALLAH,
    Restaurant.City.GAZA,
    Restaurant.City.JERUSALEM,
    Restaurant.City.NABLUS,
    Restaurant.City.BETHLEHEM,
    Restaurant.City.JERICHO,
)

# Rough bounding box for Palestine (West Bank + Gaza) map markers.
MAP_LAT_MIN = 31.0
MAP_LAT_MAX = 33.5
MAP_LNG_MIN = 34.0
MAP_LNG_MAX = 35.9

VISIBLE_REVIEW_FILTER = Q(reviews__is_visible=True)


def annotate_public_stats(queryset: QuerySet) -> QuerySet:
    """Add average rating and review count (visible reviews only)."""
    return queryset.annotate(
        avg_rating=Avg("reviews__rating", filter=VISIBLE_REVIEW_FILTER),
        visible_review_count=Count("reviews", filter=VISIBLE_REVIEW_FILTER),
    )


def get_active_restaurants() -> QuerySet:
    """Base queryset for customer-facing restaurant listings."""
    return (
        Restaurant.objects.filter(status=Restaurant.Status.ACTIVE)
        .select_related("category")
        .prefetch_related("tags", "images")
    )


def filter_restaurants(
    queryset: QuerySet,
    *,
    q: str = "",
    city: str = "",
    category_id: str = "",
) -> QuerySet:
    """Apply search and filter query parameters."""
    if q:
        queryset = queryset.filter(
            Q(name_en__icontains=q)
            | Q(name_ar__icontains=q)
            | Q(description_en__icontains=q)
            | Q(description_ar__icontains=q)
        )
    if city:
        queryset = queryset.filter(city=city)
    if category_id:
        try:
            queryset = queryset.filter(category_id=int(category_id))
        except (TypeError, ValueError):
            pass
    return queryset


def get_public_restaurant_list(
    *,
    q: str = "",
    city: str = "",
    category_id: str = "",
) -> QuerySet:
    qs = annotate_public_stats(get_active_restaurants())
    return filter_restaurants(qs, q=q, city=city, category_id=category_id)


def get_top_rated_restaurants(limit: int = 4) -> QuerySet:
    """Highest-rated active restaurants; unrated listings appear last."""
    return (
        annotate_public_stats(get_active_restaurants())
        .order_by(
            F("avg_rating").desc(nulls_last=True),
            "-visible_review_count",
            "-pk",
        )[:limit]
    )


def get_public_restaurant_detail(pk: int) -> Restaurant:
    menu_items = MenuItem.objects.filter(is_available=True).order_by("order", "name_en")
    menu_categories = MenuCategory.objects.prefetch_related(
        Prefetch("items", queryset=menu_items),
    ).order_by("order", "name_en")
    return (
        get_active_restaurants()
        .prefetch_related(
            Prefetch("categories", queryset=menu_categories),
            Prefetch(
                "reviews",
                queryset=Review.objects.filter(is_visible=True)
                .select_related("user")
                .prefetch_related("replies__user")
                .order_by("-created_at"),
            ),
        )
        .get(pk=pk)
    )


def get_filter_categories() -> QuerySet:
    return (
        RestaurantCategory.objects.filter(
            restaurants__status=Restaurant.Status.ACTIVE,
        )
        .distinct()
        .order_by("order", "name_en")
    )


def get_map_restaurants(queryset: QuerySet | None = None) -> QuerySet:
    """Restaurants with valid GPS inside Palestine — for map markers."""
    qs = queryset if queryset is not None else get_active_restaurants()
    return (
        qs.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .filter(
            latitude__gte=MAP_LAT_MIN,
            latitude__lte=MAP_LAT_MAX,
            longitude__gte=MAP_LNG_MIN,
            longitude__lte=MAP_LNG_MAX,
        )
    )


def get_landing_stats() -> dict[str, int]:
    """Platform counters for the homepage stats bar."""
    active = Restaurant.objects.filter(status=Restaurant.Status.ACTIVE)
    rated = annotate_public_stats(active).filter(avg_rating__gte=4.0)

    return {
        "restaurants": active.count(),
        "reviews": Review.objects.filter(
            is_visible=True,
            restaurant__status=Restaurant.Status.ACTIVE,
        ).count(),
        "users": CustomUser.objects.filter(is_active=True).count(),
        "top_rated": rated.count(),
    }


def get_landing_review_highlights(
    *,
    limit_restaurants: int = 3,
    reviews_per: int = 2,
) -> list[dict]:
    """Top-rated restaurants with their latest visible reviews (homepage modal)."""
    top = list(get_top_rated_restaurants(limit=limit_restaurants))
    if not top:
        return []
    pks = [r.pk for r in top]
    reviews = (
        Review.objects.filter(is_visible=True, restaurant_id__in=pks)
        .select_related("user", "restaurant", "restaurant__category")
        .order_by("-created_at")
    )
    by_restaurant: dict[int, list] = {pk: [] for pk in pks}
    for review in reviews:
        bucket = by_restaurant[review.restaurant_id]
        if len(bucket) < reviews_per:
            bucket.append(review)
    return [
        {"restaurant": restaurant, "reviews": by_restaurant[restaurant.pk]}
        for restaurant in top
        if by_restaurant[restaurant.pk]
    ]


def get_rating_breakdown(restaurant: Restaurant) -> list[dict]:
    """Return star distribution counts (5 down to 1) for the reviews tab."""
    rows = (
        restaurant.reviews.filter(is_visible=True)
        .values("rating")
        .annotate(count=Count("id"))
    )
    counts = {row["rating"]: row["count"] for row in rows}
    total = sum(counts.values()) or 1
    breakdown = []
    for stars in range(5, 0, -1):
        count = counts.get(stars, 0)
        breakdown.append(
            {
                "stars": stars,
                "count": count,
                "pct": round(count / total * 100),
            }
        )
    return breakdown
