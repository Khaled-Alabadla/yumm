"""
ai_bot/services/search.py
Simple restaurant search (beginner-friendly version)
"""

from django.db.models import Avg, Count, Q


def query_restaurants(user_message: str):
    """
    Simple search based on text, city, price, and keywords.
    No intents, no complexity.
    """

    from restaurants.models import Restaurant

    msg = user_message.lower()

    qs = (
        Restaurant.objects
        .filter(status=Restaurant.Status.ACTIVE)
        .select_related("category")
        .prefetch_related("tags", "menu_items", "images")
        .annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        )
    )

  
    city_map = {
        "نابلس": "nablus",
        "غزة": "gaza",
        "رام الله": "ramallah",
        "القدس": "jerusalem",
        "الخليل": "hebron",
        "بيت لحم": "bethlehem",
        "جنين": "jenin",
    }

    for key, val in city_map.items():
        if key in msg:
            qs = qs.filter(city=val)
            break

    # ─────────────────────────────
    # 2. PRICE FILTER
    # ─────────────────────────────
    if any(w in msg for w in ["رخيص", "cheap", "budget", "اقتصادي"]):
        qs = qs.filter(price_range=1)

    elif any(w in msg for w in ["متوسط", "medium", "moderate"]):
        qs = qs.filter(price_range=2)

    elif any(w in msg for w in ["غالي", "expensive", "luxury"]):
        qs = qs.filter(price_range=3)

    # ─────────────────────────────
    # 3. OPEN NOW FILTER
    # ─────────────────────────────
    if any(w in msg for w in ["مفتوح", "open", "open now", "هلق"]):
        qs = qs.filter(is_open=True)

  
    if msg:
        qs = qs.filter(
            Q(name_en__icontains=msg) |
            Q(name_ar__icontains=msg) |
            Q(category__name_en__icontains=msg) |
            Q(category__name_ar__icontains=msg) |
            Q(tags__name_en__icontains=msg) |
            Q(tags__name_ar__icontains=msg) |
            Q(description_en__icontains=msg) |
            Q(description_ar__icontains=msg)
        ).distinct()

    results = qs.order_by("-avg_rating", "-review_count")[:5]

    return [_enrich(r) for r in results]


def _enrich(r) -> dict:
    """
    Convert restaurant object → simple dict for frontend + AI
    """

    primary_img = r.images.filter(is_primary=True).first()

    return {
        "id": r.id,
        "name": r.name_en,
        "city": r.get_city_display(),
        "category": r.category.name_en if r.category else "General",
        "tags": ", ".join(t.name_en for t in r.tags.all()),
        "rating": round(r.avg_rating, 1) if r.avg_rating else None,
        "review_count": r.review_count,
        "price_range": r.price_range,
        "is_open": r.is_open,
        "image": primary_img.image.url if primary_img else None,
        "url": f"/restaurants/{r.id}/",

        # optional simple fields for AI
        "description": (r.description_en or "")[:150],
    }