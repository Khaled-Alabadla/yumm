from .language import reply_language

BASE = (
    "You are Yumm AI, a restaurant assistant for the Yumm platform in Palestine.\n"
    "You MUST respond in the SAME language the user writes in.\n"
    "Be friendly and conversational.\n\n"
)

FORMAT_RULE = """
FORMATTING RULES:
- Write in plain conversational text only. Do NOT use Markdown.
- NEVER use **bold**, bullet points with "-", numbered lists, headers, or ">" blockquotes.
- Write normal sentences, like a person texting a friend a recommendation.
"""

TRUST_DATA_RULE = """
DATA TRUST RULE:
- Every field in the RESTAURANTS block comes directly from the Yumm database right now.
- The Open / Closed status, prices, ratings, and menu items are 100% accurate.
- NEVER add disclaimers like "please call to confirm" or "verify before going".
- Do NOT invent, guess, or add any restaurant names, prices, or details not in the list.
"""

STRICT_RULE = """
CRITICAL RULES — NEVER BREAK THESE:
1. You can ONLY recommend restaurants from the list provided below.
2. If no restaurants are provided → say clearly that no matches were found. NEVER invent names.
3. NEVER mention restaurant names not in the list.
4. Only state facts that appear in the restaurant data below.
"""

LANG_HINT = """
LANGUAGE: respond ONLY in the same language as the user's last message.
Arabic message → Arabic response. English message → English response.
"""


def build_narrative_prompt(
    *,
    user_message: str,
    restaurants: list | None,
    parsed_context: str,
    focus_label: str,
) -> str:
    """Prompt for Together AI — rewrite DB facts into natural prose only."""
    lang = reply_language(user_message)
    lang_name = "Arabic" if lang == "ar" else "English"

    style_ar = """
STYLE (Arabic):
- اكتب عربية فصحى بسيطة وسلسة، واضحة ومباشرة.
- لا تستخدم لغة ركيكة أو ترجمة حرفية.
- اذكر بالضبط ما طلبه المستخدم (مثلاً "الكنافة" وليس "حلويات" إذا طلب كنافة).
- 2-3 فقرات قصيرة كحد أقصى، جملة أو جملتان لكل مطعم.
- لا تكرر اسم المدينة مرتين في نفس الجملة.
- التقييم بصيغة: 5 من 5 (بدون فاصلة عشرية).
"""
    style_en = """
STYLE (English):
- Write clear, friendly, concise prose.
- 2-3 short paragraphs max, one or two sentences per restaurant.
- Mention exactly what the user asked for.
"""

    if not restaurants:
        return (
            BASE
            + f"\nOUTPUT LANGUAGE: {lang_name} ONLY. Never mix languages.\n"
            + (style_ar if lang == "ar" else style_en)
            + FORMAT_RULE
            + STRICT_RULE
            + (f"\nCONTEXT:\n{parsed_context}\n" if parsed_context else "")
            + f"\nUSER SEARCH FOCUS: {focus_label}\n"
            + "NO RESTAURANTS IN DATABASE.\n"
            + "TASK: Say honestly that nothing matched. Suggest trying another city or wording.\n"
        )

    rest_section = _format_restaurants(restaurants)

    return (
        BASE
        + f"\nOUTPUT LANGUAGE: {lang_name} ONLY. Never mix languages.\n"
        + (style_ar if lang == "ar" else style_en)
        + FORMAT_RULE
        + STRICT_RULE
        + TRUST_DATA_RULE
        + (f"\nCONTEXT:\n{parsed_context}\n" if parsed_context else "")
        + f"\nUSER SEARCH FOCUS: {focus_label}\n"
        + "RESTAURANTS (USE ONLY THESE — do not add or invent any):\n"
        + rest_section
        + "\nTASK:\n"
        + "- Write a natural recommendation using ONLY the data above.\n"
        + "- Match the user's specific request (focus), not a broader category.\n"
        + "- Include: name, city, open/closed, rating, one relevant dish with price if listed.\n"
        + "- Do NOT list with bullets or numbers. Use flowing sentences.\n"
        + "- Restaurant detail cards appear below your message — keep text concise.\n"
    )


def build_greeting_prompt() -> str:
    return (
        BASE
        + LANG_HINT
        + FORMAT_RULE
        + "\nTASK: The user just greeted you — they did NOT ask about a specific restaurant yet.\n"
        + "Reply warmly and briefly, then ask what kind of food, city, budget, or occasion "
        + "they're interested in.\n"
        + "Do NOT say anything about restaurants not being found — no search has happened yet.\n"
    )


def build_prompt(
    user_message: str,
    restaurants: list | None = None,
    parsed_context: str = "",
) -> str:
    if not restaurants:
        return (
            BASE
            + LANG_HINT
            + FORMAT_RULE
            + STRICT_RULE
            + (f"\nUSER REQUEST CONTEXT:\n{parsed_context}\n" if parsed_context else "")
            + "\nNO RESTAURANTS FOUND IN DATABASE.\n"
            + "TASK: Tell the user honestly that no restaurants matched their request.\n"
            + "Suggest they try a different city, food type, or budget.\n"
            + "Do NOT invent or suggest any restaurant names.\n"
        )

    rest_section = _format_restaurants(restaurants)

    return (
        BASE
        + LANG_HINT
        + FORMAT_RULE
        + STRICT_RULE
        + TRUST_DATA_RULE
        + (f"\nUSER REQUEST CONTEXT:\n{parsed_context}\n" if parsed_context else "")
        + "\nRESTAURANTS FROM DATABASE (USE ONLY THESE):\n"
        + rest_section
        + "\nTASK:\n"
        + "- Recommend the best matching restaurants from the list above ONLY.\n"
        + "- Explain clearly why each one fits the user's request (food type, city, budget, etc.).\n"
        + "- If menu items and prices are listed, mention relevant dishes and whether they fit the budget.\n"
        + "- Mention ratings and open/closed status when useful.\n"
        + "- Recommend ALL matching restaurants from the list (up to what is provided).\n"
        + "- NEVER add restaurants outside this list.\n"
    )


def build_follow_up_prompt(restaurants: list) -> str:
    rest_section = _format_restaurants(restaurants)
    return (
        BASE
        + LANG_HINT
        + FORMAT_RULE
        + STRICT_RULE
        + TRUST_DATA_RULE
        + "\nRESTAURANTS THE USER IS ASKING ABOUT:\n"
        + rest_section
        + "\nTASK:\n"
        + "- The user is asking a follow-up about one or more of these restaurants.\n"
        + "- Answer using ONLY the data below.\n"
        + "- If they ask to compare, compare only these restaurants.\n"
        + "- NEVER mention restaurants not in this list.\n"
    )


def format_parsed_context(parsed, user_message: str = "") -> str:
    use_ar = reply_language(user_message) == "ar"
    lines = []
    if getattr(parsed, "primary_term", ""):
        lines.append(
            f"طلب المستخدم تحديداً: {parsed.primary_term}"
            if use_ar
            else f"User specifically asked for: {parsed.primary_term}"
        )
    if parsed.city:
        lines.append(
            f"المدينة: {parsed.city}" if use_ar else f"City filter: {parsed.city}"
        )
    if parsed.food_groups:
        groups = ", ".join(parsed.food_groups)
        lines.append(f"نوع الأكل: {groups}" if use_ar else f"Food type: {groups}")
    if parsed.party_size:
        lines.append(
            f"عدد الأشخاص: {parsed.party_size}"
            if use_ar
            else f"Party size: {parsed.party_size} people"
        )
    if parsed.budget_total:
        if parsed.party_size:
            lines.append(
                f"الميزانية: {parsed.budget_total}₪ "
                f"({int(parsed.per_person_budget or 0)}₪ للشخص)"
                if use_ar
                else (
                    f"Total budget: {parsed.budget_total}₪ "
                    f"({int(parsed.per_person_budget or 0)}₪ per person)"
                )
            )
        else:
            lines.append(
                f"الميزانية: {parsed.budget_total}₪"
                if use_ar
                else f"Budget: {parsed.budget_total}₪"
            )
    if parsed.price_range:
        if use_ar:
            labels = {1: "اقتصادي", 2: "متوسط", 3: "فاخر"}
        else:
            labels = {1: "Budget", 2: "Moderate", 3: "Expensive"}
        label = labels.get(parsed.price_range, str(parsed.price_range))
        lines.append(
            f"مستوى السعر: {label}" if use_ar else f"Price level: {label}"
        )
    if parsed.open_now:
        lines.append("مفتوح الآن" if use_ar else "Only open restaurants requested")
    if parsed.family_friendly:
        lines.append("مناسب للعائلة" if use_ar else "Family-friendly requested")
    return "\n".join(lines)


def _format_restaurants(restaurants: list) -> str:
    lines = []
    for i, r in enumerate(restaurants, 1):
        line = (
            f"{i}. {r['name']} | {r['city']} | {r['category']}\n"
            f"   Rating: {r['rating'] or 'No ratings'} ({r['review_count']} reviews)\n"
            f"   Price level: {r['price_range']} | {'Open' if r['is_open'] else 'Closed'}\n"
        )
        if r.get("avg_price") is not None:
            line += (
                f"   Menu prices: avg {r['avg_price']}₪"
                f" (min {r['min_price']}₪, max {r['max_price']}₪)\n"
            )
        if r.get("budget_note"):
            line += f"   Budget fit: {r['budget_note']}\n"
        if r.get("tags"):
            line += f"   Tags: {r['tags']}\n"
        if r.get("menu_items"):
            line += f"   Menu: {r['menu_items']}\n"
        if r.get("description"):
            line += f"   Description: {r['description']}\n"
        lines.append(line)
    return "\n".join(lines)
