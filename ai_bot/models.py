from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Session #{self.pk} — {self.user}"
    

class ChatMessage(models.Model):

    class Role(models.TextChoices):
        USER      = "user",      _("User")
        ASSISTANT = "assistant", _("Assistant")

    session    = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role       = models.CharField(max_length=10, choices=Role.choices)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"