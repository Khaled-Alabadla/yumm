"""Review, rating, notification, and wishlist models."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """
    A user's 1–5 star rating and written comment for a restaurant.

    The ``unique_together`` constraint ensures each user can submit exactly
    one review per restaurant; further edits update the existing record.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
        verbose_name=_("user"),
        help_text=_("The user who wrote this review."),
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("restaurant"),
    )
    rating = models.PositiveSmallIntegerField(
        _("rating"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_("Star rating from 1 (worst) to 5 (best)."),
    )
    comment = models.TextField(
        _("comment"),
        help_text=_("Written feedback about the restaurant."),
    )
    is_reported = models.BooleanField(
        _("is reported"),
        default=False,
        db_index=True,
        help_text=_("Flagged by users for admin moderation."),
    )
    is_visible = models.BooleanField(
        _("is visible"),
        default=True,
        db_index=True,
        help_text=_("Uncheck to hide this review from the public site."),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name        = _("review")
        verbose_name_plural = _("reviews")
        ordering            = ["-is_reported", "-created_at"]
        # One review per user per restaurant.
        unique_together = [["user", "restaurant"]]
        indexes = [
            models.Index(fields=["restaurant", "rating"]),
            models.Index(fields=["restaurant", "created_at"]),
        ]

    def __str__(self) -> str:
        stars = f"{self.rating}★"
        return f"{self.user} → {self.restaurant} ({stars})"


class ReviewImage(models.Model):
    """
    One of potentially many photos attached to a single review.
    Customers can upload multiple images to support their written comment.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("review"),
    )
    image = models.ImageField(
        _("image"),
        upload_to="reviews/images/",
    )
    order = models.PositiveSmallIntegerField(
        _("display order"),
        default=0,
        help_text=_("Lower numbers appear first in the review image gallery."),
    )
    uploaded_at = models.DateTimeField(_("uploaded at"), auto_now_add=True)

    class Meta:
        verbose_name        = _("review image")
        verbose_name_plural = _("review images")
        ordering            = ["order", "uploaded_at"]

    def __str__(self) -> str:
        return f"Image #{self.order or self.pk} for review #{self.review_id}"


class CommentReply(models.Model):
    """
    A reply to a Review, posted by the restaurant owner or another user.
    Multiple replies per review are allowed (threaded discussion).
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("review"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_replies",
        verbose_name=_("user"),
        help_text=_("The user (owner or regular) who posted this reply."),
    )
    reply_text = models.TextField(
        _("reply text"),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name        = _("comment reply")
        verbose_name_plural = _("comment replies")
        ordering            = ["created_at"]

    def __str__(self) -> str:
        return f"Reply by {self.user} on review #{self.review_id}"


class Wishlist(models.Model):
    """
    A user's saved / favourite restaurant entry.

    The ``unique_together`` constraint prevents the same restaurant from
    appearing more than once in a user's wishlist.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
        verbose_name=_("user"),
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
        verbose_name=_("restaurant"),
    )
    created_at = models.DateTimeField(_("saved at"), auto_now_add=True)

    class Meta:
        verbose_name        = _("wishlist entry")
        verbose_name_plural = _("wishlist entries")
        ordering            = ["-created_at"]
        unique_together = [["user", "restaurant"]]

    def __str__(self) -> str:
        return f"{self.user} ♥ {self.restaurant}"


class Notification(models.Model):
    """
    An in-app notification delivered to a specific user.

    Bilingual ``text_ar`` / ``text_en`` fields let the platform render
    the message in the user's preferred language without extra queries.

    ``notification_type`` is provided for extensibility so the frontend
    can render different icons or colours per type (e.g. new review vs.
    status change).
    """

    class Type(models.TextChoices):
        NEW_REVIEW    = "new_review",    _("New Review")
        NEW_REPLY     = "new_reply",     _("New Reply")
        STATUS_CHANGE = "status_change", _("Status Change")
        GENERAL       = "general",       _("General")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("recipient"),
    )
    notification_type = models.CharField(
        _("type"),
        max_length=20,
        choices=Type.choices,
        default=Type.GENERAL,
        db_index=True,
    )
    text_ar = models.TextField(
        _("text (Arabic)"),
        help_text=_("Notification message displayed to Arabic-language users."),
    )
    text_en = models.TextField(
        _("text (English)"),
        help_text=_("Notification message displayed to English-language users."),
    )
    is_read = models.BooleanField(
        _("is read"),
        default=False,
        db_index=True,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name        = _("notification")
        verbose_name_plural = _("notifications")
        ordering            = ["-created_at"]
        indexes = [
            # Efficiently fetch all unread notifications for a given user.
            models.Index(fields=["user", "is_read", "created_at"]),
        ]

    def __str__(self) -> str:
        state = _("read") if self.is_read else _("unread")
        return f"[{self.get_notification_type_display()}] {self.user} — {state}"
