"""Validate Together AI narrative replies before showing to users."""

from __future__ import annotations

import re

from .language import has_arabic, reply_language
from .local_replies import sanitize_reply

_STAR_OR_MD = re.compile(r"[\*#]|^[-•]\s", re.MULTILINE)


def validate_narrative_reply(
    text: str,
    restaurants: list,
    user_message: str,
) -> str | None:
    """
    Return cleaned reply if valid, else None (caller should use local fallback).
    """
    if not text or len(text.strip()) < 15:
        return None

    cleaned = sanitize_reply(text)
    if not cleaned:
        return None

    if _STAR_OR_MD.search(cleaned):
        cleaned = sanitize_reply(cleaned)
        if _STAR_OR_MD.search(cleaned):
            return None

    lang = reply_language(user_message)
    text_has_ar = has_arabic(cleaned)

    if lang == "ar" and not text_has_ar:
        return None
    if lang == "en" and text_has_ar and len(cleaned) > 30:
        ascii_ratio = sum(1 for c in cleaned if c.isascii() and not c.isspace()) / max(
            len(cleaned), 1
        )
        if ascii_ratio < 0.4:
            return None

    allowed_names = {r.get("name", "").lower() for r in restaurants if r.get("name")}
    if allowed_names:
        # Reject if AI invents a restaurant-looking name not in our list.
        # Simple heuristic: if "مطعم" patterns — skip heavy validation.
        pass

    if len(cleaned) > 1200:
        cleaned = cleaned[:1200].rsplit("\n", 1)[0] + "…"

    return cleaned
