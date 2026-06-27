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
    phone = models.CharField(_("phone"), max_length=20, blank=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []  # email is already USERNAME_FIELD

    objects = CustomUserManager()

    class Meta:
        verbose_name        = _("user")
        verbose_name_plural = _("users")
        ordering            = ["-date_joined"]

    def __str__(self) -> str:
        return self.email

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
