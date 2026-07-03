"""Shared constants and helpers for restaurants app."""

from pathlib import Path

from django.conf import settings
from django.templatetags.static import static

TAG_NAME_AR = {
    "Mansaf": "منسف",
    "Musakhan": "مسخّن",
    "Family": "عائلي",
    "Grills": "مشاوي",
    "BBQ": "شواء",
    "Seafood": "مأكولات بحرية",
    "Cafe": "مقهى",
    "Breakfast": "فطور",
    "Organic": "عضوي",
    "Sweets": "حلويات",
    "Knafeh": "كنافة",
}

DISHES_DIR = (
    Path(settings.BASE_DIR) / "restaurants" / "static" / "restaurants" / "img" / "dishes"
)

COVERS_DIR = (
    Path(settings.BASE_DIR) / "restaurants" / "static" / "restaurants" / "img" / "covers"
)

# Restaurant cover photos — interiors / ambiance, no people (local static files)
CATEGORY_COVER_FILES = {
    "Traditional Palestinian": "traditional.jpg",
    "Grills & BBQ": "grills.jpg",
    "Cafe & Breakfast": "cafe.jpg",
    "Sweets": "sweets.jpg",
    "Oriental": "oriental.jpg",
    "Mediterranean": "mediterranean.jpg",
    "Alsham": "oriental.jpg",
}

CATEGORY_COVER_KEYWORDS = (
    ("grill", "grills.jpg"),
    ("bbq", "grills.jpg"),
    ("sweet", "sweets.jpg"),
    ("cafe", "cafe.jpg"),
    ("breakfast", "cafe.jpg"),
    ("seafood", "mediterranean.jpg"),
    ("mediterranean", "mediterranean.jpg"),
    ("oriental", "oriental.jpg"),
    ("palestinian", "traditional.jpg"),
    ("traditional", "traditional.jpg"),
)

DEFAULT_COVER_IMAGE = "default.jpg"

JPEG_MAGIC = b"\xff\xd8\xff"


def _is_valid_cover_file(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size < 8000:
        return False
    try:
        return path.read_bytes()[:3] == JPEG_MAGIC
    except OSError:
        return False


# One unique cover photo per demo restaurant (slug filename)
RESTAURANT_COVER_FILES = {
    "Al-Kanaan": "al-kanaan.jpg",
    "Gaza Grill House": "gaza-grill-house.jpg",
    "Jerusalem Garden Cafe": "jerusalem-garden-cafe.jpg",
    "Nablus Sweets House": "nablus-sweets-house.jpg",
    "Bethlehem Zaatar Oven": "bethlehem-zaatar-oven.jpg",
    "Jericho Dates & Grill": "jericho-dates-grill.jpg",
    "Al-Sham Kitchen": "al-sham-kitchen.jpg",
    "Hebron Heritage Kitchen": "hebron-heritage-kitchen.jpg",
    "Gaza Mediterranean Blue": "gaza-mediterranean-blue.jpg",
    "Ramallah Sweet Palace": "ramallah-sweet-palace.jpg",
    "Jerusalem Shawarma Express": "jerusalem-shawarma-express.jpg",
}

# Authentic Palestinian / Levantine dish photos (local static files)
DISH_IMAGE_FILES = {
    "Musakhan": "musakhan.jpg",
    "Mansaf": "mansaf.jpg",
    "Maqluba": "maqluba.jpg",
    "Mixed Grill Platter": "shawarma.jpg",
    "Grilled Sea Bream": "shawarma.jpg",
    "Garden Breakfast": "shakshuka.jpg",
    "Shakshuka": "shakshuka.jpg",
    "Knafeh Nabulsiyeh": "knafeh.jpg",
    "Ma'amoul Box": "knafeh.jpg",
    "Zaatar Manakish": "musakhan.jpg",
    "Labneh Plate": "musakhan.jpg",
    "Date Lamb Tagine": "mansaf.jpg",
    "Mixed Mezze": "musakhan.jpg",
    "Mixed Mezze Platter": "musakhan.jpg",
    "Shawarma Plate": "shawarma.jpg",
    "Hebron Mansaf": "mansaf.jpg",
    "Maftoul with Chicken": "maqluba.jpg",
    "Grilled Sea Bass": "shawarma.jpg",
    "Seafood Paella": "shawarma.jpg",
    "Knafeh with Cream": "knafeh.jpg",
    "Baklava Assortment": "knafeh.jpg",
    "Chicken Shawarma Wrap": "shawarma.jpg",
    "Falafel Sandwich": "falafel.jpg",
}

DISH_IMAGE_KEYWORDS = (
    ("knafeh", "knafeh.jpg"),
    ("baklava", "knafeh.jpg"),
    ("ma'amoul", "knafeh.jpg"),
    ("sweet", "knafeh.jpg"),
    ("shawarma", "shawarma.jpg"),
    ("falafel", "falafel.jpg"),
    ("hummus", "falafel.jpg"),
    ("mezze", "falafel.jpg"),
    ("grill", "shawarma.jpg"),
    ("bbq", "shawarma.jpg"),
    ("fish", "shawarma.jpg"),
    ("seafood", "shawarma.jpg"),
    ("breakfast", "shakshuka.jpg"),
    ("shakshuka", "shakshuka.jpg"),
    ("mansaf", "mansaf.jpg"),
    ("musakhan", "musakhan.jpg"),
    ("maqluba", "maqluba.jpg"),
    ("maftoul", "maqluba.jpg"),
    ("lamb", "mansaf.jpg"),
    ("chicken", "musakhan.jpg"),
    ("zaatar", "musakhan.jpg"),
    ("manakish", "musakhan.jpg"),
    ("labneh", "musakhan.jpg"),
    ("tagine", "mansaf.jpg"),
    ("rice", "maqluba.jpg"),
)

DEFAULT_DISH_IMAGE = "musakhan.jpg"


def resolve_cover_image_file(category_name_en: str) -> str:
    if category_name_en in CATEGORY_COVER_FILES:
        return CATEGORY_COVER_FILES[category_name_en]
    lower = (category_name_en or "").lower()
    for keyword, filename in CATEGORY_COVER_KEYWORDS:
        if keyword in lower:
            return filename
    return DEFAULT_COVER_IMAGE


def get_restaurant_cover_url(
    restaurant_name_en: str = "",
    category_name_en: str = "",
) -> str:
    if restaurant_name_en in RESTAURANT_COVER_FILES:
        filename = RESTAURANT_COVER_FILES[restaurant_name_en]
    else:
        filename = resolve_cover_image_file(category_name_en)
    if not _is_valid_cover_file(COVERS_DIR / filename):
        for fallback in (
            *RESTAURANT_COVER_FILES.values(),
            DEFAULT_COVER_IMAGE,
            "grills.jpg",
            "traditional.jpg",
        ):
            if _is_valid_cover_file(COVERS_DIR / fallback):
                filename = fallback
                break
    return static(f"restaurants/img/covers/{filename}")


def resolve_dish_image_file(name_en: str) -> str:
    if name_en in DISH_IMAGE_FILES:
        return DISH_IMAGE_FILES[name_en]
    lower = name_en.lower()
    for keyword, filename in DISH_IMAGE_KEYWORDS:
        if keyword in lower:
            return filename
    return DEFAULT_DISH_IMAGE


def get_dish_image_url(name_en: str) -> str:
    filename = resolve_dish_image_file(name_en)
    if not (DISHES_DIR / filename).exists():
        for fallback in ("musakhan.jpg", "mansaf.jpg", "maqluba.jpg", "knafeh.jpg", "shawarma.jpg"):
            if (DISHES_DIR / fallback).exists():
                filename = fallback
                break
    return static(f"restaurants/img/dishes/{filename}")
