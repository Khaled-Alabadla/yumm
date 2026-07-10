"""Build natural conversational replies from database results."""

from __future__ import annotations

import re

from .language import reply_language
from .search import CITY_ALIASES, ParsedQuery

_STAR_CHARS = "★☆⭐✩✪✫✬✭✮✯"
_HASHTAG = re.compile(r"#\w+")

_CRAVING_AR = {
    "cafe": "قهوة وفطور",
    "sweets": "حلويات",
    "grills": "مشاوي",
    "seafood": "مأكولات بحرية",
    "traditional": "أكلات فلسطينية",
    "oriental": "أكل شرقي",
    "mediterranean": "أكلات متوسطية",
    "family": "مطاعم عائلية",
    "fast_food": "أكل سريع",
}

_CRAVING_EN = {
    "cafe": "coffee and breakfast",
    "sweets": "sweets",
    "grills": "grills",
    "seafood": "seafood",
    "traditional": "traditional Palestinian food",
    "oriental": "oriental food",
    "mediterranean": "Mediterranean food",
    "family": "family-friendly places",
    "fast_food": "quick bites",
}

_FOCUS_AR = {
    "كنافة": "الكنافة",
    "قهوة": "القهوة",
    "شاي": "الشاي",
    "مشاوي": "المشاوي",
    "مأكولات بحرية": "المأكولات البحرية",
    "حلويات": "الحلويات",
    "منسف": "المنسف",
    "شاورما": "الشاورما",
}


def sanitize_reply(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = text.replace("**", "").replace("__", "")
    text = _HASHTAG.sub("", text)
    for ch in _STAR_CHARS:
        text = text.replace(ch, "")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _is_ar(user_message: str = "") -> bool:
    return reply_language(user_message) == "ar"


def _parse_menu_items(menu_str: str) -> list[tuple[str, str]]:
    if not menu_str:
        return []
    items = []
    for part in menu_str.split(","):
        part = part.strip()
        match = re.match(r"(.+?)\s*\(([^)]+)\)\s*$", part)
        if match:
            items.append((match.group(1).strip(), match.group(2).strip()))
        elif part:
            items.append((part, ""))
    return items


def _focus_label(parsed: ParsedQuery, user_message: str) -> str:
    if parsed.primary_term:
        term = parsed.primary_term
        if _is_ar(user_message):
            return _FOCUS_AR.get(term, term)
        return term
    if parsed.food_groups:
        group = parsed.food_groups[0]
        if _is_ar(user_message):
            return _CRAVING_AR.get(group, "مطاعم")
        return _CRAVING_EN.get(group, "restaurants")
    if _is_ar(user_message):
        return "مطاعم"
    return "restaurants"


def _format_rating(rating: float | None) -> str:
    if rating is None:
        return ""
    if float(rating).is_integer():
        return str(int(rating))
    return str(rating).rstrip("0").rstrip(".")


def _format_price(price: str) -> str:
    if not price:
        return ""
    clean = price.replace(".00", "").replace("₪", "").strip()
    return f"{clean} ₪"


def _clean_place_name(name: str, city: str) -> str:
    for sep in (" — ", " - "):
        if sep in name:
            suffix = name.split(sep, 1)[1].strip()
            if city.lower() in suffix.lower() or suffix.lower() in city.lower():
                return name.split(sep, 1)[0].strip()
    return name


def _city_in_name(name: str, city: str) -> bool:
    name_l = name.lower()
    city_l = city.lower()
    return city_l in name_l or any(part in name_l for part in city_l.split() if len(part) > 2)


def _pick_dish(r: dict, parsed: ParsedQuery) -> tuple[str, str]:
    dishes = _parse_menu_items(r.get("menu_items", ""))
    if not dishes:
        return "", ""

    focus = (parsed.primary_term or "").lower()
    if focus:
        for dish, price in dishes:
            if focus in dish.lower():
                return dish, price.replace(".00", "")

    dish, price = dishes[0]
    return dish, price.replace(".00", "")


def _suggest_sentence_ar(
    r: dict, parsed: ParsedQuery, *, position: int, total: int
) -> str:
    name = _clean_place_name(r["name"], r["city"])
    city = r["city"]
    rating = _format_rating(r.get("rating"))
    is_open = r.get("is_open")
    dish, price = _pick_dish(r, parsed)
    price_fmt = _format_price(price)

    if position == 0:
        if _city_in_name(r["name"], city):
            opener = f"في {city}، {name}"
        else:
            opener = f"في {city}، {name}"
    else:
        opener = f"وفي {city} أيضاً، {name}"

    if total > 1 and position == 0:
        opener += " من أبرز الخيارات"

    status = "مفتوح الآن" if is_open else "مغلق حالياً"
    parts = [f"{opener} — {status}"]

    if rating:
        parts.append(f"تقييمه {rating} من 5")

    line = "، ".join(parts) + "."

    if dish:
        if price_fmt:
            line += f"\nأنصحك بتجربة {dish} بسعر {price_fmt}."
        else:
            line += f"\nعندهم {dish}."

    return line


def _suggest_sentence_en(
    r: dict, parsed: ParsedQuery, *, position: int, total: int
) -> str:
    name = _clean_place_name(r["name"], r["city"])
    city = r["city"]
    rating = _format_rating(r.get("rating"))
    is_open = r.get("is_open")
    dish, price = _pick_dish(r, parsed)
    price_fmt = _format_price(price)

    if position == 0:
        opener = f"In {city}, {name}"
        if total > 1:
            opener += " is a top pick"
    else:
        opener = f"In {city}, {name} is another good option"

    status = "open now" if is_open else "closed right now"
    line = f"{opener} — {status}"

    if rating:
        line += f", rated {rating}/5"

    line += "."

    if dish:
        if price_fmt:
            line += f"\nTry the {dish} for {price_fmt}."
        else:
            line += f"\nThey serve {dish}."

    return line


def _suggest_sentence(
    r: dict, parsed: ParsedQuery, user_message: str, *, position: int, total: int
) -> str:
    if _is_ar(user_message):
        return _suggest_sentence_ar(r, parsed, position=position, total=total)
    return _suggest_sentence_en(r, parsed, position=position, total=total)


def _restaurant_intro(focus: str, user_message: str, count: int) -> str:
    if _is_ar(user_message):
        if count == 1:
            return f"بخصوص {focus}، هذا ما وجدته لك:"
        return f"بخصوص {focus}، إليك أنسب الخيارات التي وجدتها:"
    if count == 1:
        return f"For {focus}, here's what I found:"
    return f"For {focus}, here are the best matches I found:"


def off_topic_reply(user_message: str = "") -> str:
    if _is_ar(user_message):
        return "عذراً، لا أملك إجابة عن هذا السؤال."
    return "Sorry, I don't have the answer to this question."


def greeting_reply(user_message: str = "") -> str:
    if _is_ar(user_message):
        return (
            "أهلاً وسهلاً.\n\n"
            "أخبرني ماذا تبحث عنه — نوع الطعام، المدينة، أو الميزانية — "
            "وسأقترح عليك أنسب المطاعم."
        )
    return (
        "Hello.\n\n"
        "Tell me what you're looking for — food, city, or budget — "
        "and I'll suggest the best restaurants."
    )


def _city_label(city_code: str, user_message: str) -> str:
    aliases = CITY_ALIASES.get(city_code, [])
    if _is_ar(user_message):
        for alias in aliases:
            if any("\u0600" <= ch <= "\u06FF" for ch in alias):
                return alias
    for alias in aliases:
        if alias.isascii():
            return alias.title()
    return city_code.replace("_", " ").title()


def no_results_reply(parsed: ParsedQuery, user_message: str = "") -> str:
    focus = _focus_label(parsed, user_message)

    if _is_ar(user_message):
        if parsed.city:
            city = _city_label(parsed.city, user_message)
            if parsed.price_range:
                return (
                    f"لم أعثر على مطاعم تقدّم {focus} في {city} بهذا المستوى السعري.\n\n"
                    "جرّب توسيع البحث أو تغيير الميزانية."
                )
            return (
                f"لم أعثر على مطاعم تقدّم {focus} في {city}.\n\n"
                "جرّب صياغة مختلفة أو نوع طعام آخر."
            )
        if parsed.price_range and not parsed.quality_focus:
            return (
                f"لم أعثر على مطاعم فاخرة تقدّم {focus} حالياً.\n\n"
                "جرّب تحديد مدينة أو توسيع نطاق السعر."
            )
        if parsed.food_groups or parsed.primary_term:
            term = parsed.primary_term or focus
            return f"لا توجد مطاعم تقدّم {term} حالياً."
        return (
            "لم أعثر على مطاعم مطابقة لبحثك.\n\n"
            "جرّب تحديد نوع الطعام أو المدينة."
        )

    if parsed.city:
        city = _city_label(parsed.city, user_message)
        if parsed.price_range:
            return (
                f"I couldn't find restaurants serving {focus} in {city} at that price level.\n\n"
                "Try broadening your search or adjusting the budget."
            )
        return (
            f"I couldn't find restaurants serving {focus} in {city}.\n\n"
            "Try a different wording or another type of food."
        )
    if parsed.price_range and not parsed.quality_focus:
        return (
            f"I couldn't find upscale restaurants serving {focus} right now.\n\n"
            "Try adding a city or widening the price range."
        )
    if parsed.food_groups or parsed.primary_term:
        term = parsed.primary_term or focus
        return f"No restaurants serving {term} right now."
    return (
        "I couldn't find matching restaurants.\n\n"
        "Try specifying the food type or city."
    )


def restaurant_reply(
    restaurants: list, parsed: ParsedQuery, user_message: str = ""
) -> str:
    if not restaurants:
        return no_results_reply(parsed, user_message)

    focus = _focus_label(parsed, user_message)
    shown = restaurants[:3]
    intro = _restaurant_intro(focus, user_message, len(shown))

    sentences = [
        _suggest_sentence(r, parsed, user_message, position=i, total=len(shown))
        for i, r in enumerate(shown)
    ]

    result = intro + "\n\n" + "\n\n".join(sentences)

    if parsed.budget_total and parsed.party_size:
        if _is_ar(user_message):
            result += (
                f"\n\nضمن ميزانية {parsed.budget_total} ₪ لـ {parsed.party_size} أشخاص، "
                "هذه الخيارات مناسبة لكم."
            )
        else:
            result += (
                f"\n\nWith a {parsed.budget_total} ₪ budget for {parsed.party_size} people, "
                "these options should work well."
            )

    return result


def follow_up_reply(restaurants: list, user_message: str = "") -> str:
    if not restaurants:
        return no_results_reply(ParsedQuery(), user_message)

    shown = restaurants[:3]
    sentences = [
        _suggest_sentence(r, ParsedQuery(), user_message, position=i, total=len(shown))
        for i, r in enumerate(shown)
    ]

    if _is_ar(user_message):
        return "بخصوص سؤالك:\n\n" + "\n\n".join(sentences)
    return "About your question:\n\n" + "\n\n".join(sentences)
