"""Restaurant search and enrichment for the AI assistant."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from django.db.models import Avg, Count, Min, Prefetch, Q

from restaurants.querysets import VISIBLE_REVIEW_FILTER, annotate_public_stats
from restaurants.utils import is_open_now

# ---------------------------------------------------------------------------
# Greeting detection
# ---------------------------------------------------------------------------

GREETING_WORDS = {
    "مرحبا",
    "مرحباً",
    "اهلا",
    "أهلا",
    "أهلاً",
    "هلا",
    "يا هلا",
    "السلام عليكم",
    "سلام عليكم",
    "السلام",
    "سلام",
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
    "greetings",
    "salam",
}

# ---------------------------------------------------------------------------
# City aliases — longest match wins
# ---------------------------------------------------------------------------

CITY_ALIASES: dict[str, list[str]] = {
    "jerusalem": ["jerusalem", "القدس", "قدس"],
    "ramallah": ["ramallah", "رام الله", "رامالله"],
    "al_bireh": ["al-bireh", "al bireh", "البيرة", "بيرة"],
    "gaza": ["gaza city", "gaza", "غزة", "غزه"],
    "nablus": ["nablus", "نابلس"],
    "bethlehem": ["bethlehem", "بيت لحم", "بيت لحْم"],
    "hebron": ["hebron", "الخليل", "خليل"],
    "jenin": ["jenin", "جنين"],
    "jericho": ["jericho", "أريحا", "اريحا"],
    "tulkarm": ["tulkarm", "طولكرم"],
    "qalqilya": ["qalqilya", "قلقيلية", "قلقيليه"],
    "salfit": ["salfit", "سلفيت"],
    "tubas": ["tubas", "طوباس"],
    "khan_yunis": ["khan yunis", "khan_yunis", "خان يونس"],
    "rafah": ["rafah", "رفح"],
    "jabalia": ["jabalia", "جباليا"],
    "beit_lahiya": ["beit lahiya", "بيت لاهيا"],
    "beit_hanoun": ["beit hanoun", "بيت حانون"],
    "deir_al_balah": ["deir al-balah", "دير البلح"],
    "beit_jala": ["beit jala", "بيت جالا"],
    "beit_sahour": ["beit sahour", "بيت ساحور"],
    "birzeit": ["birzeit", "بيرزيت"],
}

# Flat map sorted by alias length (longest first) for detection.
_CITY_LOOKUP: list[tuple[str, str]] = sorted(
    ((alias, code) for code, aliases in CITY_ALIASES.items() for alias in aliases),
    key=lambda item: len(item[0]),
    reverse=True,
)

# ---------------------------------------------------------------------------
# Food / cuisine synonym groups
# ---------------------------------------------------------------------------

FOOD_SYNONYMS: dict[str, list[str]] = {
    "sweets": [
        "حلويات",
        "حلوي",
        "حلوة",
        "sweets",
        "sweet",
        "dessert",
        "desserts",
        "كنافة",
        "كنافه",
        "kunafa",
        "knafeh",
        "knafe",
        "baklava",
        "بقلاوة",
        "معمول",
        "maamoul",
        "ice cream",
    ],
    "grills": [
        "مشاوي",
        "شواء",
        "شاورما",
        "grill",
        "grills",
        "bbq",
        "barbecue",
        "shawarma",
        "kebab",
        "كباب",
    ],
    "seafood": [
        "بحرية",
        "بحري",
        "سمك",
        "أسماك",
        "اسماك",
        "seafood",
        "fish",
        "paella",
        "أرز بحري",
    ],
    "cafe": [
        "مقهى",
        "مقهي",
        "قهوة",
        "شاي",
        "tea",
        "chai",
        "cafe",
        "coffee",
        "breakfast",
        "فطور",
        "شكشوكة",
        "shakshuka",
    ],
    "traditional": [
        "فلسطيني",
        "فلسطينية",
        "تقليدي",
        "تقليدية",
        "palestinian",
        "traditional",
        "mansaf",
        "منسف",
        "musakhan",
        "مسخن",
        "مقلوبة",
        "maqluba",
        "maftoul",
        "مفتول",
        "zaatar",
        "زعتر",
        "manakish",
        "فطائر",
    ],
    "oriental": [
        "شرقي",
        "أكل شرقي",
        "oriental",
        "falafel",
        "فلافل",
        "hummus",
        "حمص",
        "mezze",
        "مقبلات",
    ],
    "mediterranean": [
        "متوسطي",
        "mediterranean",
    ],
    "family": [
        "عائلي",
        "عائلة",
        "عائله",
        "عائلية",
        "family",
        "kids",
        "أطفال",
        "اطفال",
        "أطفالنا",
    ],
    "fast_food": [
        "سريع",
        "ساندويش",
        "ساندوتش",
        "sandwich",
        "wrap",
    ],
}

# Reverse lookup: surface form → canonical food group.
_FOOD_LOOKUP: dict[str, str] = {}
for group, terms in FOOD_SYNONYMS.items():
    for term in terms:
        _FOOD_LOOKUP[term.lower()] = group

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
    "أين",
    "اين",
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
    "أكل",
    "طعام",
    "ميزانية",
    "بميزانية",
    "ميزانيتي",
    "نحن",
    "احنا",
    "أشخاص",
    "اشخاص",
    "شخص",
    "ناس",
    "people",
    "persons",
    "person",
    "guests",
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
    "we",
    "are",
    "our",
    "my",
    "and",
    "or",
    "و",
    "أو",
    "مع",
    "لنا",
    "لي",
}


@dataclass
class ParsedQuery:
    city: str | None = None
    city_words: set[str] = field(default_factory=set)
    budget_total: int | None = None
    party_size: int | None = None
    per_person_budget: float | None = None
    price_range: int | None = None
    quality_focus: bool = False
    open_now: bool = False
    family_friendly: bool = False
    food_groups: list[str] = field(default_factory=list)
    search_terms: list[str] = field(default_factory=list)
    primary_term: str = ""


_QUALITY_PHRASES = (
    "من الآخر",
    "من الاخر",
    "ممتاز",
    "أحسن",
    "احسن",
    "أجود",
    "اجود",
    "the best",
    "top notch",
    "amazing",
    "excellent",
    "outstanding",
)
_SPECIFIC_TERMS: list[tuple[str, str, str]] = [
    # (match_key, label_ar, label_en) — longest keys matched first
    ("كنافة", "كنافة", "knafeh"),
    ("كنافه", "كنافة", "knafeh"),
    ("knafeh", "كنافة", "knafeh"),
    ("kunafa", "كنافة", "knafeh"),
    ("knafe", "كنافة", "knafeh"),
    ("بقلاوة", "بقلاوة", "baklava"),
    ("baklava", "بقلاوة", "baklava"),
    ("منسف", "منسف", "mansaf"),
    ("mansaf", "منسف", "mansaf"),
    ("مسخن", "مسخّن", "musakhan"),
    ("musakhan", "مسخّن", "musakhan"),
    ("شاورما", "شاورما", "shawarma"),
    ("shawarma", "شاورما", "shawarma"),
    ("فلافل", "فلافل", "falafel"),
    ("falafel", "فلافل", "falafel"),
    ("قهوة", "قهوة", "coffee"),
    ("coffee", "قهوة", "coffee"),
    ("شاي", "شاي", "tea"),
    ("tea", "شاي", "tea"),
    ("مشاوي", "مشاوي", "grills"),
    ("مأكولات بحرية", "مأكولات بحرية", "seafood"),
    ("seafood", "مأكولات بحرية", "seafood"),
    ("حلويات", "حلويات", "sweets"),
    ("sweets", "حلويات", "sweets"),
]

_SPECIFIC_LOOKUP = sorted(_SPECIFIC_TERMS, key=lambda item: len(item[0]), reverse=True)


def is_greeting(user_message: str) -> bool:
    """True only for pure greetings with no food/restaurant request."""
    from .intent import is_restaurant_related

    text = user_message.strip().lower()
    if not text:
        return False

    city, _ = detect_city(user_message)
    if is_restaurant_related(user_message, has_city=bool(city)):
        return False

    parsed = parse_query(user_message)
    if (
        parsed.food_groups
        or parsed.city
        or parsed.budget_total
        or parsed.party_size
        or parsed.family_friendly
        or parsed.open_now
    ):
        return False

    if len(text.split()) <= 6:
        for word in sorted(GREETING_WORDS, key=len, reverse=True):
            if word in text:
                return True

    return False


def detect_city(user_message: str) -> tuple[str | None, set[str]]:
    msg = user_message.lower()
    for alias, code in _CITY_LOOKUP:
        if alias in msg:
            return code, set(alias.split())
    return None, set()


def parse_query(user_message: str) -> ParsedQuery:
    msg = user_message.lower().replace("sea food", "seafood")
    parsed = ParsedQuery()

    parsed.city, parsed.city_words = detect_city(user_message)

    party_match = re.search(
        r"(?:نحن|احنا|واحنا|we(?:'re| are))\s*(\d{1,2})|"
        r"(\d{1,2})\s*(?:أشخاص|اشخاص|شخص|ناس|people|persons|guests)|"
        r"for\s+(\d{1,2})\s*(?:people|persons|guests)?",
        msg,
    )
    if party_match:
        parsed.party_size = int(next(g for g in party_match.groups() if g))

    budget_match = re.search(
        r"(?:بميزانية|ميزانية|ميزانيتنا|ميزانتنا|budget(?:\s+of)?|under|less than|بحدود|حوالي|around)\s*(\d{2,4})|"
        r"(\d{2,4})\s*(?:شيكل|شواقل|₪|shekel|shekels|nis|ils)",
        msg,
    )
    if budget_match:
        parsed.budget_total = int(next(g for g in budget_match.groups() if g))

    if parsed.budget_total and parsed.party_size and parsed.party_size > 0:
        parsed.per_person_budget = parsed.budget_total / parsed.party_size
    elif parsed.budget_total:
        parsed.per_person_budget = float(parsed.budget_total)

    quality_focus = any(phrase in msg for phrase in _QUALITY_PHRASES)

    if any(w in msg for w in ("رخيص", "cheap", "budget", "اقتصادي", "low cost")):
        parsed.price_range = 1
    elif any(w in msg for w in ("متوسط", "medium", "moderate")):
        parsed.price_range = 2
    elif any(w in msg for w in ("غالي", "expensive", "luxury", "premium", "₪₪₪")):
        parsed.price_range = 3
    elif "فاخر" in msg and not quality_focus:
        parsed.price_range = 3
    elif quality_focus or "فاخر" in msg:
        parsed.quality_focus = True

    parsed.open_now = any(w in msg for w in ("مفتوح", "مفتوح الآن", "open now", "open"))
    parsed.family_friendly = any(
        w in msg for w in ("عائلي", "عائلة", "عائله", "family", "kids", "أطفال", "اطفال")
    )

    found_groups: set[str] = set()
    found_terms: set[str] = set()

    for alias, group in _FOOD_LOOKUP.items():
        if alias in msg:
            found_groups.add(group)
            found_terms.add(alias)

    for group, synonyms in FOOD_SYNONYMS.items():
        for synonym in synonyms:
            if synonym.lower() in msg:
                found_groups.add(group)
                found_terms.add(synonym.lower())

    parsed.food_groups = sorted(found_groups)
    parsed.search_terms = sorted(found_terms)

    for key, label_ar, label_en in _SPECIFIC_LOOKUP:
        if key in msg:
            from .language import reply_language

            parsed.primary_term = (
                label_ar if reply_language(user_message) == "ar" else label_en
            )
            break

    if not parsed.food_groups:
        tokens = [
            w
            for w in re.findall(r"[\w\u0600-\u06FF]+", msg)
            if w not in STOP_WORDS
            and w not in parsed.city_words
            and len(w) >= 2
            and not w.isdigit()
        ]
        parsed.search_terms = tokens[:6]

    return parsed


def _menu_stats(restaurant) -> dict:
    prices = [
        float(item.price)
        for item in restaurant.menu_items.all()
        if item.is_available and item.price is not None
    ]
    if not prices:
        return {
            "min_price": None,
            "max_price": None,
            "avg_price": None,
        }
    return {
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": round(sum(prices) / len(prices), 1),
    }


def _matches_food_group(restaurant, group: str) -> bool:
    category_en = (restaurant.category.name_en if restaurant.category else "").lower()
    category_ar = (restaurant.category.name_ar if restaurant.category else "").lower()
    tags = [t.name_en.lower() for t in restaurant.tags.all()] + [
        t.name_ar.lower() for t in restaurant.tags.all()
    ]

    group_terms = [t.lower() for t in FOOD_SYNONYMS.get(group, [])] + [group]

    haystack = " ".join(
        [
            category_en,
            category_ar,
            " ".join(tags),
            (restaurant.description_en or "").lower(),
            (restaurant.description_ar or "").lower(),
        ]
    )

    for item in restaurant.menu_items.all():
        haystack += f" {(item.name_en or '').lower()} {(item.name_ar or '').lower()}"

    return any(term in haystack for term in group_terms)


def _matches_search_term(restaurant, term: str) -> bool:
    term = term.lower()
    fields = [
        restaurant.name_en,
        restaurant.name_ar or "",
        restaurant.category.name_en if restaurant.category else "",
        restaurant.category.name_ar if restaurant.category else "",
        restaurant.description_en or "",
        restaurant.description_ar or "",
    ]
    fields.extend(t.name_en for t in restaurant.tags.all())
    fields.extend(t.name_ar for t in restaurant.tags.all())
    fields.extend(item.name_en for item in restaurant.menu_items.all())
    fields.extend(item.name_ar for item in restaurant.menu_items.all())

    return any(term in (value or "").lower() for value in fields)


def _score_restaurant(restaurant, parsed: ParsedQuery) -> int:
    score = 0
    stats = _menu_stats(restaurant)

    if parsed.city:
        if restaurant.city == parsed.city:
            score += 20
        else:
            return 0

    if parsed.price_range and restaurant.price_range == parsed.price_range:
        score += 8
    elif parsed.price_range and restaurant.price_range:
        score -= abs(restaurant.price_range - parsed.price_range) * 2

    if parsed.quality_focus:
        score += int((restaurant.avg_rating or 0) * 4)
        score += min(restaurant.visible_review_count or 0, 8)

    if parsed.open_now and not is_open_now(restaurant):
        score -= 8

    if parsed.family_friendly:
        family_tags = {"family", "عائلي", "عائلة"}
        tag_names = {t.name_en.lower() for t in restaurant.tags.all()} | {
            t.name_ar for t in restaurant.tags.all()
        }
        if family_tags & tag_names or _matches_food_group(restaurant, "family"):
            score += 6

    if parsed.primary_term:
        term = parsed.primary_term.lower()
        for item in restaurant.menu_items.all():
            names = f"{(item.name_ar or '').lower()} {(item.name_en or '').lower()}"
            if term in names:
                score += 15
                break
        else:
            haystack = " ".join(
                [
                    (restaurant.name_ar or "").lower(),
                    (restaurant.name_en or "").lower(),
                    (restaurant.description_ar or "").lower(),
                    (restaurant.description_en or "").lower(),
                ]
            )
            for tag in restaurant.tags.all():
                haystack += f" {tag.name_ar.lower()} {tag.name_en.lower()}"
            if term in haystack:
                score += 8

    if parsed.food_groups:
        group_hits = sum(1 for group in parsed.food_groups if _matches_food_group(restaurant, group))
        if group_hits == 0:
            return 0
        score += group_hits * 10
    elif parsed.search_terms:
        term_hits = sum(1 for term in parsed.search_terms if _matches_search_term(restaurant, term))
        if term_hits == 0 and parsed.city:
            score += 1
        elif term_hits == 0:
            return 0
        else:
            score += term_hits * 5

    if parsed.per_person_budget is not None and stats["avg_price"] is not None:
        if stats["avg_price"] <= parsed.per_person_budget:
            score += 8
        elif stats["min_price"] is not None and stats["min_price"] <= parsed.per_person_budget:
            score += 5
        else:
            score -= 6

    rating = restaurant.avg_rating or 0
    score += int(rating * 2)
    score += min(restaurant.visible_review_count or 0, 10)

    return score


def _base_queryset():
    from restaurants.models import MenuItem, Restaurant

    menu_qs = MenuItem.objects.filter(is_available=True).order_by("order", "name_en")
    return annotate_public_stats(
        Restaurant.objects.filter(status=Restaurant.Status.ACTIVE)
        .select_related("category")
        .prefetch_related("tags", "images", Prefetch("menu_items", queryset=menu_qs))
        .annotate(
            menu_avg_price=Avg("menu_items__price", filter=Q(menu_items__is_available=True)),
            menu_min_price=Min("menu_items__price", filter=Q(menu_items__is_available=True)),
        )
    )


def query_restaurants(user_message: str) -> tuple[list[dict], ParsedQuery]:
    """Search active restaurants and return enriched results plus parsed filters."""
    parsed = parse_query(user_message)
    qs = _base_queryset()

    if parsed.city:
        qs = qs.filter(city=parsed.city)

    if parsed.per_person_budget is not None:
        qs = qs.filter(
            Q(menu_min_price__lte=parsed.per_person_budget)
            | Q(menu_avg_price__lte=parsed.per_person_budget)
        ).distinct()

    candidates = list(qs)
    scored = [(r, _score_restaurant(r, parsed)) for r in candidates]
    scored = [(r, s) for r, s in scored if s > 0]
    scored.sort(key=lambda item: item[1], reverse=True)

    if not scored and parsed.city and not parsed.food_groups and not parsed.search_terms:
        fallback = list(
            _base_queryset()
            .filter(city=parsed.city)
            .order_by("-avg_rating", "-visible_review_count")[:5]
        )
        return [_enrich(r, parsed) for r in fallback], parsed

    top = [r for r, _ in scored[:5]]
    return [_enrich(r, parsed) for r in top], parsed


def fetch_restaurants_by_ids(restaurant_ids: list) -> list[dict]:
    """Load specific restaurants for follow-up questions."""
    if not restaurant_ids:
        return []

    from restaurants.models import Restaurant

    qs = _base_queryset().filter(id__in=restaurant_ids)
    by_id = {r.id: r for r in qs}
    ordered = [by_id[i] for i in restaurant_ids if i in by_id]
    return [_enrich(r, ParsedQuery()) for r in ordered]


def _enrich(restaurant, parsed: ParsedQuery) -> dict:
    from django.utils.translation import get_language

    lang = get_language() or "en"
    use_ar = lang.startswith("ar")

    primary_img = restaurant.images.filter(is_primary=True).first()
    stats = _menu_stats(restaurant)

    menu_items = ", ".join(
        f"{(item.name_ar if use_ar and item.name_ar else item.name_en)} ({item.price}₪)"
        for item in restaurant.menu_items.all()[:8]
    )

    price_label = (
        {1: "اقتصادي (₪)", 2: "متوسط (₪₪)", 3: "فاخر (₪₪₪)"}.get(
            restaurant.price_range, "غير محدد"
        )
        if use_ar
        else {1: "Budget (₪)", 2: "Moderate (₪₪)", 3: "Expensive (₪₪₪)"}.get(
            restaurant.price_range, "Not specified"
        )
    )

    name = restaurant.name_ar if use_ar and restaurant.name_ar else restaurant.name_en
    category = ""
    if restaurant.category:
        category = (
            restaurant.category.name_ar
            if use_ar and restaurant.category.name_ar
            else restaurant.category.name_en
        )

    description = (
        (restaurant.description_ar if use_ar else restaurant.description_en)
        or restaurant.description_en
        or restaurant.description_ar
        or ""
    )[:180]

    rating = round(restaurant.avg_rating, 1) if restaurant.avg_rating else None
    stars = ""
    if rating:
        full = int(round(rating))
        stars = "★" * full + "☆" * (5 - full)

    from restaurants.constants import TAG_NAME_AR

    tags_list = []
    for t in restaurant.tags.all():
        if use_ar and t.name_en in TAG_NAME_AR:
            tags_list.append(TAG_NAME_AR[t.name_en])
        elif use_ar and t.name_ar:
            tags_list.append(t.name_ar)
        else:
            tags_list.append(t.name_en)

    budget_note = ""
    if parsed.budget_total:
        if parsed.party_size:
            budget_note = (
                f"Fits ~{parsed.party_size} people with ~{int(parsed.budget_total)}₪ total "
                f"(~{int(parsed.per_person_budget or 0)}₪/person)"
            )
        else:
            budget_note = f"Budget target: ~{parsed.budget_total}₪"

    return {
        "id": restaurant.id,
        "name": name,
        "name_en": restaurant.name_en,
        "name_ar": restaurant.name_ar or restaurant.name_en,
        "city": restaurant.get_city_display(),
        "category": category or "General",
        "tags": ", ".join(tags_list),
        "tags_list": tags_list,
        "rating": rating,
        "stars": stars,
        "review_count": restaurant.visible_review_count or 0,
        "price_range": price_label,
        "is_open": is_open_now(restaurant),
        "image": primary_img.image.url if primary_img else None,
        "url": f"/restaurants/{restaurant.id}/",
        "description": description,
        "menu_items": menu_items,
        "min_price": stats["min_price"],
        "max_price": stats["max_price"],
        "avg_price": stats["avg_price"],
        "budget_note": budget_note,
        "lat": float(restaurant.latitude) if restaurant.latitude else None,
        "lng": float(restaurant.longitude) if restaurant.longitude else None,
    }
