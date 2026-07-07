"""Custom user model with role-based access control."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Email-primary user model.

    ``username`` is removed so that email is the single unique identifier.
    The ``role`` field drives all permission checks across the platform.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        OWNER = "owner", _("Owner")
        USER  = "user",  _("User")

    username = None  # replaced by email as USERNAME_FIELD

    email      = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name  = models.CharField(_("last name"),  max_length=150, blank=True)
    role = models.CharField(
        _("role"),
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        db_index=True,
    )
    is_approved = models.BooleanField(
        _("approved"),
        default=False,
        db_index=True,
        help_text=_(
            "Restaurant owners must be approved by an admin before they can operate on the platform."
        ),
    )
    
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    city = models.CharField(_("city"), max_length=30, blank=True, db_index=True)
    address = models.CharField(_("address"), max_length=500, blank=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []  # email is already USERNAME_FIELD

    objects = CustomUserManager()

    class Meta:
        verbose_name        = _("user")
        verbose_name_plural = _("users")
        ordering            = ["-date_joined"]

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        if self.role != self.Role.OWNER:
            self.is_approved = True
        elif not self.pk:
            self.is_approved = False
        else:
            old_role = (
                CustomUser.objects.filter(pk=self.pk)
                .values_list("role", flat=True)
                .first()
            )
            if old_role and old_role != self.Role.OWNER:
                self.is_approved = False
        super().save(*args, **kwargs)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    @property
    def full_name(self) -> str:
        """
        Return "First Last".
        Falls back to the email local part when both name fields are blank,
        matching the single "Full Name" field shown in the registration design.
        """
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email.split("@")[0]

    # ------------------------------------------------------------------
    # Role-check helpers  (avoids raw string comparisons in other modules)
    # ------------------------------------------------------------------

    @property
    def is_admin_role(self) -> bool:
        return self.role == self.Role.ADMIN

    @property
    def is_owner_role(self) -> bool:
        return self.role == self.Role.OWNER

    @property
    def is_plain_user(self) -> bool:
        return self.role == self.Role.USER

    @property
    def is_pending_owner(self) -> bool:
        return self.is_owner_role and not self.is_approved


class ContactMessage(models.Model):
    """Inbound message from the public contact form."""

    class Subject(models.TextChoices):
        RESTAURANT_PARTNERSHIP = "Restaurant Partnership", _("Restaurant Partnership")
        TECHNICAL_SUPPORT = "Technical Support", _("Technical Support")
        MEDIA_PRESS = "Media & Press", _("Media & Press")
        GENERAL_INQUIRY = "General Inquiry", _("General Inquiry")

    name = models.CharField(_("full name"), max_length=100)
    email = models.EmailField(_("email address"))
    subject = models.CharField(
        _("subject"),
        max_length=50,
        choices=Subject.choices,
        db_index=True,
    )
    message = models.TextField(_("message"), max_length=1000)
    is_read = models.BooleanField(
        _("read"),
        default=False,
        db_index=True,
        help_text=_("Mark when the message has been reviewed."),
    )
    created_at = models.DateTimeField(_("received at"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("contact message")
        verbose_name_plural = _("contact messages")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} — {self.get_subject_display()}"
