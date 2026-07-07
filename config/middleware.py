"""Middleware that serves branded error pages in development and production."""

from __future__ import annotations

from django.conf import settings


class CustomErrorPageMiddleware:
    """
    Use Yumm 403/404 templates even when DEBUG=True.

    Django skips handler404/handler403 while DEBUG is on and returns its
    yellow debug pages instead. This middleware replaces those responses
    for normal browser navigation.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not getattr(settings, "YUMM_CUSTOM_ERROR_PAGES", True):
            return response
        if response.status_code not in (403, 404):
            return response
        if not self._wants_html_page(request):
            return response

        from config.error_views import page_not_found, permission_denied

        if response.status_code == 404:
            return page_not_found(request, None)
        return permission_denied(request, None)

    @staticmethod
    def _wants_html_page(request) -> bool:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return False

        accept = request.headers.get("Accept", "")
        if "text/html" not in accept and "*/*" not in accept:
            return False
        if "application/json" in accept and "text/html" not in accept:
            return False

        return True
