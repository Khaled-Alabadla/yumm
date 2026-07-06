from django.urls import path
from .views import AIAssistantView, AIChatView

app_name = "ai_bot"

urlpatterns = [
    path("",      AIAssistantView.as_view(), name="assistant"),
    path("chat/", AIChatView.as_view(),      name="chat"),
]