import json
import traceback

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from .services import get_ai_response
from .models import ChatSession, ChatMessage


class AIAssistantView(TemplateView):
    template_name = "ai_bot/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["previous_messages"] = []
        context["session_id"] = None

        if self.request.user.is_authenticated:
            session = (
                ChatSession.objects.filter(user=self.request.user)
                .order_by("-updated_at")
                .first()
            )

            if session:
                context["session_id"] = session.id

                context["previous_messages"] = [
                    {
                        "role": msg.role,
                        "content": msg.content,
                    }
                    for msg in session.messages.all()
                ]

        return context


@method_decorator(csrf_exempt, name="dispatch")
class AIChatView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)

            user_message = body.get("message", "").strip()
            history = body.get("history", [])
            last_restaurants = body.get("last_restaurants", [])

            if not user_message:
                return JsonResponse(
                    {"error": "Message is required"},
                    status=400,
                )

            if request.user.is_authenticated and not history:
                history = self._load_history(request.user)

            result = get_ai_response(
                user_message=user_message,
                history=history,
                last_restaurants=last_restaurants,
            )

            if request.user.is_authenticated:
                session = self._get_or_create_session(request.user)

                self._save_messages(
                    session=session,
                    user_message=user_message,
                    ai_reply=result["reply"],
                )

                result["session_id"] = session.id

            return JsonResponse(result)

        except Exception as e:
            traceback.print_exc()

            return JsonResponse(
                {
                    "reply": _("Sorry, something went wrong. Please try again."),
                    "restaurants": [],
                    "error": str(e),
                },
                status=500,
            )

    def _get_or_create_session(self, user):
        session = ChatSession.objects.filter(user=user).order_by("-updated_at").first()

        if not session:
            session = ChatSession.objects.create(user=user)

        return session

    def _load_history(self, user):
        session = ChatSession.objects.filter(user=user).order_by("-updated_at").first()

        if not session:
            return []

        messages = session.messages.order_by("-created_at")[:10]

        return [
            {
                "role": m.role,
                "content": m.content,
            }
            for m in reversed(list(messages))
        ]

    def _save_messages(self, session, user_message, ai_reply):
        ChatMessage.objects.create(
            session=session,
            role=ChatMessage.Role.USER,
            content=user_message,
        )

        ChatMessage.objects.create(
            session=session,
            role=ChatMessage.Role.ASSISTANT,
            content=ai_reply,
        )

        session.save()
