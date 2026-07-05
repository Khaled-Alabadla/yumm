"""
ai_bot/services/ai_client.py
Simple Together AI caller (safe & minimal version)
"""

import time
import logging
from together import Together

logger = logging.getLogger("ai_bot")

TOGETHER_MODEL = "openai/gpt-oss-20b"


def call_ai(
    system_prompt: str,
    user_message: str,
    history: list,
    max_tokens: int = 700,
    temperature: float = 0.6,
) -> str:
    """
    Call Together AI and return response text safely.
    """

    try:
        client = Together()

        safe_history = history[-4:] if history else []

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(safe_history)
        messages.append({"role": "user", "content": user_message})

        start = time.time()

        response = client.chat.completions.create(
            model=TOGETHER_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        elapsed = round(time.time() - start, 2)

        reply = response.choices[0].message.content.strip()

        logger.info(f"[AI] response_time={elapsed}s")

        return reply

    except Exception as e:
        logger.error(f"[AI ERROR] {str(e)}")

        return (
            "Sorry, I couldn't process your request right now. "
            "Please try again in a moment."
        )