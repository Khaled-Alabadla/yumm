import time
import logging

from django.template.loader import render_to_string
from django.utils import translation

from .intent import classify_intent
from .language import reply_language
from .search import (
    detect_city,
    fetch_restaurants_by_ids,
    is_greeting,
    parse_query,
    query_restaurants,
)
from .prompts import (
    build_narrative_prompt,
    format_parsed_context,
)
from .ai_client import call_ai, is_ai_available
from .ai_validate import validate_narrative_reply
from .local_replies import (
    _focus_label,
    follow_up_reply,
    greeting_reply,
    no_results_reply,
    off_topic_reply,
    restaurant_reply,
    sanitize_reply,
)

logger = logging.getLogger("ai_bot")


def _try_ai_narrative(
    *,
    user_message: str,
    history: list,
    restaurants: list,
    parsed,
    local_fallback: str,
    focus_label: str,
) -> str:
    """Use Together AI to narrate DB results; fall back to local reply on any issue."""
    if not is_ai_available():
        return local_fallback

    context = format_parsed_context(parsed, user_message)
    prompt = build_narrative_prompt(
        user_message=user_message,
        restaurants=restaurants,
        parsed_context=context,
        focus_label=focus_label,
    )

    raw = call_ai(
        system_prompt=prompt,
        user_message=user_message,
        history=history,
        max_tokens=450,
        temperature=0.35,
    )

    validated = validate_narrative_reply(raw, restaurants, user_message)
    if validated:
        logger.info("[AI] narrative reply accepted")
        return validated

    logger.warning("[AI] narrative reply rejected — using local fallback")
    return local_fallback


def get_ai_response(
    user_message: str, history: list = None, last_restaurants: list = None
):
    if history is None:
        history = []
    if last_restaurants is None:
        last_restaurants = []

    lang = reply_language(user_message)

    with translation.override(lang):
        return _build_response(user_message, history, last_restaurants)


def _build_response(
    user_message: str, history: list, last_restaurants: list
) -> dict:
    start = time.time()
    greeting = is_greeting(user_message)
    city, _ = detect_city(user_message)

    intent = classify_intent(
        user_message,
        last_restaurants=last_restaurants,
        has_city=bool(city),
        is_greeting=greeting,
    )

    restaurants = []
    parsed = parse_query(user_message)
    question_type = intent
    confidence = 0.9
    used_ai = False

    if intent == "off_topic":
        execution_ms = int((time.time() - start) * 1000)
        return {
            "reply": sanitize_reply(off_topic_reply(user_message)),
            "restaurants": [],
            "restaurants_html": [],
            "question_type": "off_topic",
            "confidence": 1.0,
            "execution_ms": execution_ms,
            "ai_narrated": False,
        }

    if intent == "greeting":
        reply = greeting_reply(user_message)

    elif intent == "follow_up":
        ids = [r.get("id") for r in last_restaurants if r.get("id")]
        restaurants = fetch_restaurants_by_ids(ids)
        local = follow_up_reply(restaurants, user_message)
        focus = _focus_label(parsed, user_message)
        ai_reply = _try_ai_narrative(
            user_message=user_message,
            history=history,
            restaurants=restaurants,
            parsed=parsed,
            local_fallback=local,
            focus_label=focus,
        )
        reply = ai_reply
        used_ai = ai_reply != local and is_ai_available()

    else:
        restaurants, parsed = query_restaurants(user_message)
        local = restaurant_reply(restaurants, parsed, user_message)
        focus = _focus_label(parsed, user_message)

        if restaurants:
            ai_reply = _try_ai_narrative(
                user_message=user_message,
                history=history,
                restaurants=restaurants,
                parsed=parsed,
                local_fallback=local,
                focus_label=focus,
            )
            reply = ai_reply
            used_ai = ai_reply != local and is_ai_available()
            confidence = 0.92
        else:
            reply = no_results_reply(parsed, user_message)
            confidence = 0.75

    restaurants_html = []
    for r in restaurants:
        html = render_to_string(
            "ai_bot/components/restaurant_card.html", {"restaurant": r}
        )
        restaurants_html.append(html)

    execution_ms = int((time.time() - start) * 1000)

    return {
        "reply": sanitize_reply(reply),
        "restaurants": restaurants,
        "restaurants_html": restaurants_html,
        "question_type": question_type,
        "confidence": confidence,
        "execution_ms": execution_ms,
        "ai_narrated": used_ai,
    }
