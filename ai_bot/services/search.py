import re

from django.db.models import Avg, Count, Q

STOP_WORDS = {
    "بدي",
    "ابي",
    "اريد",
    "اعطني",
    "اقترح",
    "ابحث",
    "عن",
    "في",
    "بـ",
    "من",
    "على",
    "هل",
    "شو",
    "وين",
    "كيف",
    "مطعم",
    "مطاعم",
    "فيه",
    "عنده",
    "عندو",
    "يقدم",
    "يعمل",
    "فيها",
    "هناك",
    "يكون",
    "ممكن",
    "بدنا",
    "نبحث",
    "الي",
    "تحت",
    "اقل",
    "واقل",
    "بحدود",
    "شيكل",
    "شواقل",
    "وجبة",
    "وجبات",
    "غذاء",
    "غدا",
    "غداء",
    "عشاء",
    "فطور",
    "اكل",
    "طعام",
    "ميزانية",
    "بميزانية",
    "ميزانيتي",
    "i",
    "want",
    "find",
    "me",
    "a",
    "an",
    "the",
    "in",
    "at",
    "for",
    "that",
    "restaurant",
    "restaurants",
    "has",
    "have",
    "serve",
    "serves",
    "with",
    "good",
    "nice",
    "looking",
    "need",
    "can",
    "you",
    "please",
    "where",
    "suggest",
    "give",
    "show",
    "make",
    "making",
    "which",
    "any",
    "under",
    "less",
    "than",
    "around",
    "meal",
    "food",
    "budget",
}

GREETING_WORDS = {
    "مرحبا",
    "مرحباً",
    "اهلا",
    "أهلا",
    "هلا",
    "هاي",
    "يا هلا",
    "السلام عليكم",
    "صباح الخير",
    "مساء الخير",
    "كيفك",
    "شلونك",
    "كيف الحال",
    "شخبارك",
    "hello",
    "hi",
    "hey",
    "howdy",
    "good morning",
    "good evening",
}

CITY_MAP = {
    "نابلس": "nablus",
    "nablus": "nablus",
    "غزة": "gaza",
    "gaza": "gaza",
    "رام الله": "ramallah",
    "ramallah": "ramallah",
    "القدس": "jerusalem",
    "jerusalem": "jerusalem",
    "الخليل": "hebron",
    "hebron": "hebron",
    "بيت لحم": "bethlehem",
    "bethlehem": "bethlehem",
    "جنين": "jenin",
    "jenin": "jenin",
    "طولكرم": "tulkarm",
    "tulkarm": "tulkarm",
    "أريحا": "jericho",
    "jericho": "jericho",
    "خان يونس": "khan_yunis",
    "khan yunis": "khan_yunis",
    "رفح": "rafah",
    "rafah": "rafah",
}


def is_greeting(user_message: str) -> bool:
    text = user_message.strip().lower()
    if not text:
        return False

    if len(text.split()) <= 4:
        for g in GREETING_WORDS:
            if g in text:
                return True

    return False


def query_restaurants(user_message: str) -> list:
    from restaurants.models import Restaurant

    msg = user_message.lower()

    base_qs = Restaurant.objects.filter(status=Restaurant.Status.ACTIVE)

    detected_city = None
    detected_city_words = set()

    for key, val in CITY_MAP.items():
        if key in msg:
            detected_city = val
            detected_city_words = set(key.split())
            break

    if detected_city:
        base_qs = base_qs.filter(city=detected_city)

    if any(w in msg for w in ["رخيص", "cheap", "budget", "اقتصادي"]):
        base_qs = base_qs.filter(price_range=1)
    elif any(w in msg for w in ["متوسط", "medium", "moderate"]):
        base_qs = base_qs.filter(price_range=2)
    elif any(w in msg for w in ["غالي", "expensive", "luxury"]):
        base_qs = base_qs.filter(price_range=3)

    price_match = re.search(r"(\d+)", msg)
    if price_match and any(
        w in msg
        for w in ["تحت", "اقل", "under", "less than", "بحدود", "less", "around"]
    ):
        max_price = int(price_match.group(1))
        base_qs = base_qs.filter(menu_items__price__lte=max_price).distinct()

    if any(w in msg for w in ["مفتوح", "open now"]):
        base_qs = base_qs.filter(is_open=True)

    words = [
        w
        for w in msg.split()
        if w not in STOP_WORDS
        and w not in detected_city_words
        and len(w) >= 2
        and not w.isdigit()
    ]

    if words:
        q_filter = Q()
        for word in words:
            q_filter |= Q(name_en__icontains=word)
            q_filter |= Q(name_ar__icontains=word)
            q_filter |= Q(category__name_en__icontains=word)
            q_filter |= Q(category__name_ar__icontains=word)
            q_filter |= Q(tags__name_en__icontains=word)
            q_filter |= Q(tags__name_ar__icontains=word)
            q_filter |= Q(menu_items__name_en__icontains=word)
            q_filter |= Q(menu_items__name_ar__icontains=word)
        base_qs = base_qs.filter(q_filter)

    matching_ids = list(base_qs.values_list("id", flat=True).distinct())

    qs = (
        Restaurant.objects.filter(id__in=matching_ids)
        .select_related("category")
        .prefetch_related("tags", "menu_items", "images")
        .annotate(
            avg_rating=Avg("reviews__rating"),
            total_reviews=Count("reviews", distinct=True),
        )
    )

    results = qs.order_by("-avg_rating", "-total_reviews")[:5]
    return [_enrich(r) for r in results]


def _enrich(r) -> dict:
    from restaurants.utils import is_open_now

    primary_img = r.images.filter(is_primary=True).first()

    menu_items = ", ".join(
        f"{item.name_en} ({item.price}₪)"
        for item in r.menu_items.filter(is_available=True)[:8]
    )

    price_label = {
        1: "Budget (₪)",
        2: "Moderate (₪₪)",
        3: "Expensive (₪₪₪)",
    }.get(r.price_range, "Not specified")

    name = r.name_ar if r.name_ar else r.name_en

    description = (r.description_ar or r.description_en or "")[:150]

    rating = round(r.avg_rating, 1) if r.avg_rating else None

    if rating:
        full = int(round(rating))
        stars = "★" * full + "☆" * (5 - full)
    else:
        stars = ""

    tags_list = [t.name_en for t in r.tags.all()]

    return {
        "id": r.id,
        "name": name,
        "name_en": r.name_en,
        "name_ar": r.name_ar or r.name_en,
        "city": r.get_city_display(),
        "category": r.category.name_en if r.category else "General",
        "tags": ", ".join(tags_list),
        "tags_list": tags_list,
        "rating": rating,
        "stars": stars,
        "review_count": r.total_reviews,
        "price_range": price_label,
        "is_open": is_open_now(r),
        "image": primary_img.image.url if primary_img else None,
        "url": f"/restaurants/{r.id}/",
        "description": description,
        "menu_items": menu_items,
        "lat": float(r.latitude) if r.latitude else None,
        "lng": float(r.longitude) if r.longitude else None,
    }
