from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView


class AIAssistantView(TemplateView):
    template_name = "ai_bot/index.html"


class AIChatView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "message": "AI service is under development."
        })