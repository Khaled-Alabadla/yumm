"""Transactional email helpers for Yumm (verification + owner approval)."""

from __future__ import annotations

import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


def _site_url() -> str:
    return getattr(settings, "SITE_URL", "http://127.0.0.1:8000").rstrip("/")


def _absolute_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{_site_url()}{path}"


def _email_locale_context(lang: str | None = None) -> dict:
    code = (lang or translation.get_language() or "en")[:2]
    is_ar = code == "ar"
    return {
        "email_lang": "ar" if is_ar else "en",
        "email_dir": "rtl" if is_ar else "ltr",
        "email_align": "right" if is_ar else "left",
        "site_url": _site_url(),
    }


def _user_display_name(user) -> str:
    name = (getattr(user, "full_name", None) or "").strip()
    if name:
        return name
    first = (user.first_name or "").strip()
    if first:
        return first
    return user.email.split("@")[0]


def _send_branded_email(
    *,
    to_email: str,
    subject: str,
    text_template: str,
    html_template: str,
    context: dict,
) -> bool:
    text_body = render_to_string(text_template, context)
    html_body = render_to_string(html_template, context)
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    message.attach_alternative(html_body, "text/html")
    try:
        sent = message.send(fail_silently=False)
        logger.info(
            "Yumm email sent=%s to=%s subject=%s backend=%s",
            sent,
            to_email,
            subject,
            settings.EMAIL_BACKEND,
        )
        return bool(sent)
    except Exception:
        logger.exception("Failed to send email to %s (%s)", to_email, subject)
        return False


def build_verification_url(user, request=None) -> str:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    path = reverse("accounts:verify_email", kwargs={"uidb64": uid, "token": token})
    if request is not None:
        return request.build_absolute_uri(path)
    return _absolute_url(path)


def send_user_verification_email(user, request=None) -> bool:
    """Send email-confirmation link to a regular user after registration."""
    lang = translation.get_language() or "en"
    ctx = _email_locale_context(lang)
    ctx.update(
        {
            "email_title": _("Confirm your Yumm email"),
            "user_name": _user_display_name(user),
            "verify_url": build_verification_url(user, request),
        }
    )
    with translation.override(lang):
        subject = str(_("Confirm your Yumm email"))
    return _send_branded_email(
        to_email=user.email,
        subject=subject,
        text_template="emails/verify_email.txt",
        html_template="emails/verify_email.html",
        context=ctx,
    )


def send_owner_approved_email(user, restaurant=None) -> bool:
    """Notify a restaurant owner that their registration was approved."""
    lang = translation.get_language() or "en"
    restaurant_name = ""
    if restaurant is not None:
        if lang.startswith("ar"):
            restaurant_name = restaurant.name_ar or restaurant.name_en or ""
        else:
            restaurant_name = restaurant.name_en or restaurant.name_ar or ""

    ctx = _email_locale_context(lang)
    ctx.update(
        {
            "email_title": _("Your restaurant was approved"),
            "user_name": _user_display_name(user),
            "restaurant_name": restaurant_name,
            "login_url": _absolute_url(reverse("accounts:login")),
        }
    )
    with translation.override(lang):
        subject = str(_("Your restaurant was approved — welcome to Yumm"))
    return _send_branded_email(
        to_email=user.email,
        subject=subject,
        text_template="emails/owner_approved.txt",
        html_template="emails/owner_approved.html",
        context=ctx,
    )
