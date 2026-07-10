import time
import logging
from django.template.loader import render_to_string

from .search import query_restaurants, is_greeting
from .prompts import build_prompt, build_greeting_prompt
from .ai_client import call_ai

logger = logging.getLogger("ai_bot")


def get_ai_response(
    user_message: str, history: list = None, last_restaurants: list = None
):
    if history is None:
        history = []
    if last_restaurants is None:
        last_restaurants = []

    start = time.time()

    if is_greeting(user_message):
        restaurants = []
        system_prompt = build_greeting_prompt()
    else:
        restaurants = query_restaurants(user_message)

        system_prompt = build_prompt(
            user_message=user_message,
            restaurants=restaurants,
        )

    reply = call_ai(
        system_prompt=system_prompt,
        user_message=user_message,
        history=history,
    )

    restaurants_html = []
    for r in restaurants:
        html = render_to_string(
            "ai_bot/components/restaurant_card.html", {"restaurant": r}
        )
        restaurants_html.append(html)

    execution_ms = int((time.time() - start) * 1000)

    return {
        "reply": reply,
        "restaurants": restaurants,
        "restaurants_html": restaurants_html,
        "question_type": "restaurant",
        "confidence": 0.85,
        "execution_ms": execution_ms,
    }
