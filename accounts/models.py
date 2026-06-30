"""Custom user model with role-based access control."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

# from ai_bot.management.seed_restaurants import User

from .managers import CustomUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

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


# restaurants/models.py

class City(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class CuisineTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    CATEGORY_CHOICES = [
        ('traditional', 'Traditional Palestinian'),
        ('grills', 'Grills & BBQ'),
        ('cafe', 'Cafe & Breakfast'),
        ('sweets', 'Sweets & Desserts'),
        ('mediterranean', 'Mediterranean'),
        ('seafood', 'Seafood'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='traditional')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    address = models.CharField(max_length=300)
    working_hours_open = models.TimeField()
    working_hours_close = models.TimeField()
    cover_image = models.ImageField(upload_to='restaurants/covers/', blank=True)
    cover_image_url = models.URLField(blank=True)
    tags = models.ManyToManyField(CuisineTag, blank=True)
    is_open = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    def review_count(self):
        return self.reviews.count()

    def rating_distribution(self):
        dist = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        total = self.reviews.count()
        if total == 0:
            return dist
        for r in self.reviews.all():
            dist[r.rating] = dist.get(r.rating, 0) + 1
        return {k: round((v / total) * 100) for k, v in dist.items()}

    def working_hours_display(self):
        return f"{self.working_hours_open.strftime('%I:%M %p')} - {self.working_hours_close.strftime('%I:%M %p')}"


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_categories')
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu/items/', blank=True)
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ₪{self.price}"


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['restaurant', 'user']

    def __str__(self):
        return f"{self.user.full_name} - {self.restaurant.name} ({self.rating}★)"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts_wishlist')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='accounts_wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'restaurant']

    def __str__(self):
        return f"{self.user.username} → {self.restaurant.name}"


