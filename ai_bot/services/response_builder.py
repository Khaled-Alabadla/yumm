"""
ai_bot/services/response_builder.py
Simplified AI pipeline — returns Django-rendered restaurant cards.
"""

import time
import logging
from django.template.loader import render_to_string

from .search import query_restaurants
from .prompts import build_prompt
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

    # ─────────────────────────────
    # 1. SIMPLE INTENT DETECTION
    # ─────────────────────────────
    msg = user_message.lower()

    if any(word in msg for word in ["menu", "منيو"]):
        intent = "menu"
        question_type = "restaurant"

    elif any(word in msg for word in ["where", "location", "وين"]):
        intent = "location"
        question_type = "restaurant"

    elif any(word in msg for word in ["open", "مفتوح", "ساعات"]):
        intent = "working_hours"
        question_type = "restaurant"

    elif any(word in msg for word in ["compare", "مقارنة"]):
        intent = "compare"
        question_type = "restaurant"

    else:
        intent = "recommend"
        question_type = "restaurant"


    restaurants = query_restaurants(user_message)


    system_prompt = build_prompt(
        user_message=user_message,
        restaurants=restaurants,
        review_summary="",
    )

    reply = call_ai(
        system_prompt=system_prompt, user_message=user_message, history=history
    )

  
    restaurants_html = []

    for restaurant in restaurants:
        html = render_to_string(
            "ai_bot/components/restaurant_card.html", {"restaurant": restaurant}
        )
        restaurants_html.append(html)

  
    execution_ms = int((time.time() - start) * 1000)

    return {
        "reply": reply,
        "restaurants_html": restaurants_html,  # 👈 IMPORTANT FIX
        "question_type": question_type,
        "intent": intent,
        "confidence": 0.85,
        "execution_ms": execution_ms,
    }
