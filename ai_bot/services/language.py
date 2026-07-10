"""Detect reply language from user message or site locale."""

from __future__ import annotations

from django.utils.translation import get_language


def has_arabic(text: str) -> bool:
    return any("\u0600" <= ch <= "\u06FF" or "\u0750" <= ch <= "\u077F" for ch in text)


def reply_language(user_message: str = "") -> str:
    """Return 'ar' or 'en' — prefers the language the user wrote in."""
    if user_message and has_arabic(user_message):
        return "ar"
    site_lang = get_language() or "en"
    if site_lang.startswith("ar"):
        return "ar"
    return "en"
