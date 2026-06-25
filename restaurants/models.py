"""Restaurant profile and menu models."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class RestaurantCategory(models.Model):
    """
    High-level cuisine / restaurant type shown on the listing card.
    (e.g. "Traditional Palestinian", "Grills & BBQ", "Cafe & Breakfast")
    """

    name_ar = models.CharField(_("name (Arabic)"),  max_length=100)
    name_en = models.CharField(_("name (English)"), max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(
        _("display order"),
        default=0,
        help_text=_("Lower numbers appear first in filter menus."),
    )

    class Meta:
        verbose_name        = _("restaurant category")
        verbose_name_plural = _("restaurant categories")
        ordering            = ["order", "name_en"]

    def __str__(self) -> str:
        return self.name_en


class Tag(models.Model):
    """
    Keyword tag that can be attached to many restaurants.
    (e.g. "Mansaf", "Family", "Outdoor Seating", "Seafood", "Organic")
    """

    name_ar = models.CharField(_("name (Arabic)"),  max_length=50)
    name_en = models.CharField(_("name (English)"), max_length=50, unique=True)

    class Meta:
        verbose_name        = _("tag")
        verbose_name_plural = _("tags")
        ordering            = ["name_en"]

    def __str__(self) -> str:
        return self.name_en


class Restaurant(models.Model):
    """
    Core restaurant profile owned by a user with role == 'owner'.

    Bilingual ``*_ar`` / ``*_en`` fields carry the Arabic and English
    versions of every customer-facing string so the platform can serve
    both languages without extra joins.
    """

    # ------------------------------------------------------------------
    # City choices — full Palestine list
    # ------------------------------------------------------------------

    class City(models.TextChoices):
        # ── West Bank ─────────────────────────────────────────────────
        JERUSALEM    = "jerusalem",    _("Jerusalem")
        AL_RAM       = "al_ram",       _("Al-Ram")
        BEIT_HANINA  = "beit_hanina",  _("Beit Hanina")
        AL_EIZARIYA  = "al_eizariya",  _("Al-Eizariya")
        ABU_DIS      = "abu_dis",      _("Abu Dis")
        KAFR_AQAB    = "kafr_aqab",    _("Kafr Aqab")
        RAMALLAH     = "ramallah",     _("Ramallah")
        AL_BIREH     = "al_bireh",     _("Al-Bireh")
        BIRZEIT      = "birzeit",      _("Birzeit")
        SILWAD       = "silwad",       _("Silwad")
        BEIT_RIMA    = "beit_rima",    _("Beit Rima")
        DEIR_DIBWAN  = "deir_dibwan",  _("Deir Dibwan")
        BEIT_SIRA    = "beit_sira",    _("Beit Sira")
        JERICHO      = "jericho",      _("Jericho")
        AL_AUJA      = "al_auja",      _("Al-Auja")
        BETHLEHEM    = "bethlehem",    _("Bethlehem")
        BEIT_JALA    = "beit_jala",    _("Beit Jala")
        BEIT_SAHOUR  = "beit_sahour",  _("Beit Sahour")
        BEIT_FAJJAR  = "beit_fajjar",  _("Beit Fajjar")
        HUSAN        = "husan",        _("Husan")
        NAHALIN      = "nahalin",      _("Nahalin")
        HEBRON       = "hebron",       _("Hebron")
        YATTA        = "yatta",        _("Yatta")
        DURA         = "dura",         _("Dura")
        HALHUL       = "halhul",       _("Halhul")
        IDHNA        = "idhna",        _("Idhna")
        TARQUMIYYA   = "tarqumiyya",   _("Tarqumiyya")
        SURIF        = "surif",        _("Surif")
        SAIR         = "sair",         _("Sa'ir")
        BEIT_UMMAR   = "beit_ummar",   _("Beit Ummar")
        DHAHRIYA     = "dhahriya",     _("Ad-Dhahriya")
        NABLUS       = "nablus",       _("Nablus")
        SEBASTIA     = "sebastia",     _("Sebastia")
        BEIT_FURIK   = "beit_furik",   _("Beit Furik")
        BEITA        = "beita",        _("Beita")
        AQRABA       = "aqraba",       _("Aqraba")
        JENIN        = "jenin",        _("Jenin")
        QABATIYA     = "qabatiya",     _("Qabatiya")
        YABAD        = "yabad",        _("Ya'bad")
        ARRABA       = "arraba",       _("Arraba")
        BURQIN       = "burqin",       _("Burqin")
        TUBAS        = "tubas",        _("Tubas")
        TAMOUN       = "tamoun",       _("Tamoun")
        TULKARM      = "tulkarm",      _("Tulkarm")
        ANABTA       = "anabta",       _("Anabta")
        BEIT_IBA     = "beit_iba",     _("Beit Iba")
        QALQILYA     = "qalqilya",     _("Qalqilya")
        AZZUN        = "azzun",        _("Azzun")
        KAFR_THULTH  = "kafr_thulth",  _("Kafr Thulth")
        SALFIT       = "salfit",       _("Salfit")
        HARIS        = "haris",        _("Haris")
        KAFR_AL_DIK  = "kafr_al_dik",  _("Kafr ad-Dik")
        # ── Gaza Strip ────────────────────────────────────────────────
        JABALIA      = "jabalia",      _("Jabalia")
        BEIT_LAHIYA  = "beit_lahiya",  _("Beit Lahiya")
        BEIT_HANOUN  = "beit_hanoun",  _("Beit Hanoun")
        GAZA         = "gaza",         _("Gaza City")
        NUSEIRAT     = "nuseirat",     _("Nuseirat")
        BUREIJ       = "bureij",       _("Bureij")
        MAGHAZI      = "maghazi",      _("Maghazi")
        DEIR_AL_BALAH = "deir_al_balah", _("Deir al-Balah")
        KHAN_YUNIS   = "khan_yunis",   _("Khan Yunis")
        ABASAN       = "abasan",       _("Abasan")
        BANI_SUHEILA = "bani_suheila", _("Bani Suheila")
        KHUZA_A      = "khuza_a",      _("Khuza'a")
        RAFAH        = "rafah",        _("Rafah")
        TEL_AL_SULTAN = "tel_al_sultan", _("Tel al-Sultan")

    # ------------------------------------------------------------------
    # Admin-controlled approval status
    # ------------------------------------------------------------------

    class Status(models.TextChoices):
        PENDING  = "pending",  _("Pending")
        ACTIVE   = "active",   _("Active")
        REJECTED = "rejected", _("Rejected")

    # ------------------------------------------------------------------
    # Price range
    # ------------------------------------------------------------------

    class PriceRange(models.IntegerChoices):
        BUDGET     = 1, _("Budget (₪)")
        MODERATE   = 2, _("Moderate (₪₪)")
        EXPENSIVE  = 3, _("Expensive (₪₪₪)")

    # ------------------------------------------------------------------
    # Ownership & categorisation
    # ------------------------------------------------------------------

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurants",
        verbose_name=_("owner"),
        help_text=_("The restaurant-owner account that manages this listing."),
        db_index=True,
    )
    category = models.ForeignKey(
        RestaurantCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurants",
        verbose_name=_("category"),
        help_text=_("Cuisine / restaurant type shown on listing cards."),
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="restaurants",
        verbose_name=_("tags"),
        help_text=_("Searchable keywords displayed under the restaurant card."),
    )

    # ------------------------------------------------------------------
    # Bilingual identity
    # ------------------------------------------------------------------

    name_ar = models.CharField(_("name (Arabic)"),  max_length=255)
    name_en = models.CharField(_("name (English)"), max_length=255)
    description_ar = models.TextField(_("description (Arabic)"),  blank=True)
    description_en = models.TextField(_("description (English)"), blank=True)

    # ------------------------------------------------------------------
    # Location
    # ------------------------------------------------------------------

    address_ar = models.CharField(_("address (Arabic)"),  max_length=500)
    address_en = models.CharField(_("address (English)"), max_length=500)
    city = models.CharField(
        _("city"),
        max_length=30,
        choices=City.choices,
        db_index=True,
    )
    latitude = models.DecimalField(
        _("latitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_("GPS latitude coordinate (e.g. 31.900000)."),
    )
    longitude = models.DecimalField(
        _("longitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_("GPS longitude coordinate (e.g. 35.200000)."),
    )

    # ------------------------------------------------------------------
    # Operating hours
    # ------------------------------------------------------------------

    working_hours_ar = models.CharField(
        _("working hours (Arabic)"),
        max_length=255,
        blank=True,
        help_text=_("e.g. الأحد–الخميس: 9ص–10م"),
    )
    working_hours_en = models.CharField(
        _("working hours (English)"),
        max_length=255,
        blank=True,
        help_text=_("e.g. Sun–Thu: 9 AM–10 PM"),
    )

    # ------------------------------------------------------------------
    # Operational & admin status
    # ------------------------------------------------------------------

    is_open = models.BooleanField(
        _("is open"),
        default=True,
        db_index=True,
        help_text=_(
            "Toggle to mark the restaurant as temporarily closed. "
            "Displayed as the green/grey Open/Closed badge on listing cards."
        ),
    )
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        help_text=_("Admin-controlled approval status of this listing."),
    )
    price_range = models.PositiveSmallIntegerField(
        _("price range"),
        choices=PriceRange.choices,
        null=True,
        blank=True,
        help_text=_("Rough price indicator shown as bar icons on listing cards."),
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name        = _("restaurant")
        verbose_name_plural = _("restaurants")
        ordering            = ["-created_at"]
        indexes = [
            models.Index(fields=["city",   "status"]),
            models.Index(fields=["status", "is_open"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self) -> str:
        return self.name_en or self.name_ar

    # ------------------------------------------------------------------
    # Computed display helpers
    # (For listing pages, annotate with Avg/Count in the view queryset
    #  to avoid N+1 queries; these properties are for single-object use.)
    # ------------------------------------------------------------------

    @property
    def primary_image(self) -> "RestaurantImage | None":
        """
        Return the primary RestaurantImage for this restaurant, or None.
        For listing pages use select_related / prefetch_related instead.
        """
        return self.images.filter(is_primary=True).first()

    @property
    def average_rating(self) -> float | None:
        """Return the mean star rating, or None if no reviews exist."""
        agg = self.reviews.aggregate(avg=models.Avg("rating"))
        return round(agg["avg"], 1) if agg["avg"] is not None else None

    @property
    def review_count(self) -> int:
        """Return the total number of reviews for this restaurant."""
        return self.reviews.count()


class RestaurantImage(models.Model):
    """
    One of potentially many photos associated with a restaurant.

    ``image_type`` separates the cover photo (hero banner), the profile /
    logo image, and general gallery shots so templates can query each slot
    independently with ``restaurant.images.filter(image_type=...)``.

    ``is_primary`` marks the single featured image shown on listing cards.
    The ``save()`` override enforces the one-primary-per-restaurant rule
    automatically — no manual cleanup required in views or forms.
    """

    class ImageType(models.TextChoices):
        COVER   = "cover",   _("Cover Photo")
        PROFILE = "profile", _("Profile / Logo")
        GALLERY = "gallery", _("Gallery")

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("restaurant"),
    )
    image = models.ImageField(
        _("image"),
        upload_to="restaurants/images/",
    )
    image_type = models.CharField(
        _("image type"),
        max_length=10,
        choices=ImageType.choices,
        default=ImageType.GALLERY,
        db_index=True,
    )
    is_primary = models.BooleanField(
        _("is primary"),
        default=False,
        db_index=True,
        help_text=_(
            "Mark this image as the featured photo shown on listing cards. "
            "Only one image per restaurant can be primary."
        ),
    )
    caption_ar = models.CharField(_("caption (Arabic)"),  max_length=255, blank=True)
    caption_en = models.CharField(_("caption (English)"), max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(
        _("display order"),
        default=0,
        help_text=_("Lower numbers appear first in the gallery."),
    )
    uploaded_at = models.DateTimeField(_("uploaded at"), auto_now_add=True)

    class Meta:
        verbose_name        = _("restaurant image")
        verbose_name_plural = _("restaurant images")
        # Primary images first, then by explicit order.
        ordering = ["-is_primary", "order", "uploaded_at"]
        indexes  = [
            models.Index(fields=["restaurant", "is_primary"]),
            models.Index(fields=["restaurant", "image_type"]),
        ]

    def save(self, *args, **kwargs):
        # Enforce the one-primary-per-restaurant invariant before saving.
        if self.is_primary:
            RestaurantImage.objects.filter(
                restaurant_id=self.restaurant_id,
                is_primary=True,
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"{self.get_image_type_display()} — {self.restaurant}"
            f"{' ★' if self.is_primary else ''}"
        )


class MenuCategory(models.Model):
    """A named grouping of menu items (e.g. "Starters", "Mains", "Desserts")."""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name=_("restaurant"),
    )
    name_ar = models.CharField(_("name (Arabic)"),  max_length=150)
    name_en = models.CharField(_("name (English)"), max_length=150)
    order = models.PositiveSmallIntegerField(
        _("display order"),
        default=0,
        help_text=_("Lower numbers appear first in the menu."),
    )

    class Meta:
        verbose_name        = _("menu category")
        verbose_name_plural = _("menu categories")
        ordering            = ["order", "name_en"]
        unique_together     = [["restaurant", "name_en"]]

    def __str__(self) -> str:
        return f"{self.name_en} — {self.restaurant}"


class MenuItem(models.Model):
    """
    A single food or beverage dish listed inside a MenuCategory.

    ``restaurant`` is stored directly (denormalized from ``category``) so
    the menu can be filtered without an extra join. It is kept consistent
    automatically in ``save()``.
    """

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name=_("restaurant"),
    )
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("category"),
    )
    name_ar        = models.CharField(_("name (Arabic)"),         max_length=255)
    name_en        = models.CharField(_("name (English)"),        max_length=255)
    description_ar = models.TextField(_("description (Arabic)"),  blank=True)
    description_en = models.TextField(_("description (English)"), blank=True)
    price = models.DecimalField(
        _("price"),
        max_digits=8,
        decimal_places=2,
        help_text=_("Price in ILS (₪)."),
    )
    image = models.ImageField(
        _("image"),
        upload_to="menu/items/",
        null=True,
        blank=True,
    )
    is_available = models.BooleanField(
        _("is available"),
        default=True,
        db_index=True,
        help_text=_("Uncheck to hide this item without deleting it."),
    )
    order = models.PositiveSmallIntegerField(
        _("display order"),
        default=0,
        help_text=_("Lower numbers appear first within the category."),
    )

    class Meta:
        verbose_name        = _("menu item")
        verbose_name_plural = _("menu items")
        ordering            = ["order", "name_en"]
        indexes = [
            models.Index(fields=["restaurant", "is_available"]),
            models.Index(fields=["category",   "order"]),
        ]

    def save(self, *args, **kwargs):
        if self.category_id:
            self.restaurant_id = self.category.restaurant_id
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name_en} — {self.restaurant}"
