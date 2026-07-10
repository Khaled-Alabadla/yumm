"""Classify user messages before search / LLM."""

from __future__ import annotations

# Food, dining, and Yumm-platform signals.
RESTAURANT_SIGNALS = {
    # Arabic — food & dining
    "مطعم",
    "مطاعم",
    "أكل",
    "اكل",
    "طعام",
    "غذاء",
    "غدا",
    "غداء",
    "عشاء",
    "فطور",
    "وجبة",
    "وجبات",
    "حلويات",
    "حلوي",
    "حلوة",
    "كنافة",
    "كنافه",
    "بقلاوة",
    "مشاوي",
    "شواء",
    "شاورما",
    "فلافل",
    "بحرية",
    "بحري",
    "سمك",
    "مقهى",
    "مقهي",
    "قهوة",
    "منسف",
    "مسخن",
    "مقلوبة",
    "مأكولات",
    "ماكولات",
    "طبق",
    "أطباق",
    "اطباق",
    "قائمة",
    "منيو",
    "تقييم",
    "تقييمات",
    "ميزانية",
    "شيكل",
    "شواقل",
    "سعر",
    "أسعار",
    "اسعار",
    "رخيص",
    "غالي",
    "فاخر",
    "عائلي",
    "عائلة",
    "عائله",
    "أطفال",
    "اطفال",
    "مفتوح",
    "مغلق",
    "اقترح",
    "اقتراح",
    "أفضل",
    "افضل",
    "بدي",
    "ابي",
    "اريد",
    "وين",
    "أين",
    "اين",
    "فين",
    "نبحث",
    "نلاقي",
    # English
    "restaurant",
    "restaurants",
    "food",
    "meal",
    "meals",
    "dish",
    "dishes",
    "eat",
    "eating",
    "dine",
    "dining",
    "lunch",
    "dinner",
    "breakfast",
    "sweets",
    "sweet",
    "dessert",
    "desserts",
    "kunafa",
    "knafeh",
    "knafe",
    "baklava",
    "grill",
    "grills",
    "bbq",
    "seafood",
    "fish",
    "cafe",
    "coffee",
    "shawarma",
    "falafel",
    "mansaf",
    "musakhan",
    "maqluba",
    "menu",
    "review",
    "reviews",
    "rating",
    "budget",
    "shekel",
    "shekels",
    "price",
    "prices",
    "cheap",
    "expensive",
    "luxury",
    "moderate",
    "family",
    "kids",
    "open",
    "closed",
    "suggest",
    "recommend",
    "best",
    "where",
    "looking",
    "craving",
    "hungry",
    "yumm",
}

FOLLOW_UP_SIGNALS = {
    "هذا",
    "هذه",
    "ذلك",
    "تلك",
    "الأول",
    "الاول",
    "الثاني",
    "الثالث",
    "الرابع",
    "هالمطعم",
    "هذا المطعم",
    "المطعم الأول",
    "المطعم الاول",
    "المطعم الثاني",
    "أكثر",
    "اكثر",
    "تفاصيل",
    "معلومات",
    "more about",
    "tell me more",
    "about the",
    "about this",
    "the first",
    "the second",
    "the third",
    "which one",
    "that one",
    "this one",
    "compare",
}


def is_restaurant_related(user_message: str, *, has_city: bool = False) -> bool:
    """True when the message is about food, restaurants, or dining in Palestine."""
    text = user_message.strip().lower()
    if not text:
        return False

    if has_city:
        return True

    if any(signal in text for signal in RESTAURANT_SIGNALS):
        return True

    # Any parsed food/cuisine term (e.g. "شاي؟") counts as a restaurant search.
    from .search import parse_query

    parsed = parse_query(user_message)
    if parsed.food_groups or parsed.primary_term:
        return True

    # A bare number often means budget (e.g. "200 شيكل").
    return any(ch.isdigit() for ch in text) and any(
        w in text for w in ("شيكل", "شواقل", "₪", "shekel", "budget", "ميزانية", "سعر")
    )


def is_follow_up(user_message: str, last_restaurants: list) -> bool:
    """True when the user refers to previously suggested restaurants."""
    if not last_restaurants:
        return False
    text = user_message.strip().lower()
    return any(signal in text for signal in FOLLOW_UP_SIGNALS)


def classify_intent(
    user_message: str,
    *,
    last_restaurants: list | None = None,
    has_city: bool = False,
    is_greeting: bool = False,
) -> str:
    """
    Return one of: greeting | follow_up | restaurant | off_topic
    """
    if is_greeting:
        return "greeting"

    if is_follow_up(user_message, last_restaurants or []):
        return "follow_up"

    if is_restaurant_related(user_message, has_city=has_city):
        return "restaurant"

    return "off_topic"
