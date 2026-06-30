"""
Management command to seed the database with restaurant data
matching the Figma design (Yumm - Palestine restaurant discovery platform).

Usage:
    python manage.py seed_restaurants
    python manage.py seed_restaurants --flush   (clears existing data first)
"""
import datetime
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import (
    City,
    CuisineTag,
    MenuCategory,
    MenuItem,
    Restaurant,
    Review,
)

User = get_user_model()


CITIES = ["Ramallah", "Gaza", "Jerusalem", "Nablus", "Bethlehem", "Jericho"]

TAGS = ["Traditional", "Grills", "Cafe", "Sweets", "Mediterranean",
        "BBQ", "Seafood", "Breakfast", "Organic", "Kunafa", "Desserts",
        "Family", "Outdoor", "View", "Musakhan", "Mansaf"]

# Each restaurant: name, city, category, tags, rating data, description,
# working hours, address, is_open, cover image, menu categories+items, reviews
RESTAURANTS = [
    {
        "name": "Al-Kanaan",
        "city": "Ramallah",
        "category": "traditional",
        "tags": ["Mansaf", "Musakhan", "Family"],
        "is_open": True,
        "description": (
            "Al-Kanaan is one of Ramallah's most beloved traditional "
            "Palestinian restaurants, serving authentic home-style cooking "
            "for over 20 years. Our recipes are passed down through "
            "generations, using the finest local ingredients and "
            "traditional spices from across Palestine."
        ),
        "address": "Al-Masyoun, Ramallah",
        "open_time": "12:00", "close_time": "23:00",
        "cover_image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200&q=80",
        "menu": [
            ("Mains", [
                ("Musakhan", "Roasted chicken on taboon bread with caramelised sumac onions", 45),
                ("Mansaf", "Slow-cooked lamb in fermented jameed sauce on a bed of saffron rice", 65),
                ("Maqluba", "Upside-down layered rice with chicken, aubergine and toasted nuts", 55),
            ]),
            ("Desserts", [
                ("Kunafa Nabulsiyeh", "Sweet cheese pastry soaked in syrup, topped with pistachios", 30),
            ]),
        ],
        "reviews": [
            ("Layla Hassan", 5, "Amazing musakhan! Best I've had in Ramallah. The atmosphere felt like home."),
            ("Omar Khalil", 4, "Excellent food and great portions. The mansaf was authentic and delicious."),
            ("Sara Al-Ahmad", 5, "A hidden gem! Every dish was perfectly seasoned and the staff were wonderfully warm."),
        ],
    },
    {
        "name": "Gaza Grill House",
        "city": "Gaza",
        "category": "grills",
        "tags": ["Grills", "BBQ", "Seafood"],
        "is_open": True,
        "description": (
            "Gaza Grill House brings the smoky, charcoal-grilled flavors of "
            "the coast to your table. Famous for fresh seafood and "
            "perfectly charred meats, paired with traditional Gazan spices."
        ),
        "address": "Al-Rimal, Gaza City",
        "open_time": "13:00", "close_time": "23:30",
        "cover_image_url": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=1200&q=80",
        "menu": [
            ("Mains", [
                ("Mixed Grill Platter", "Lamb kofta, chicken skewers and beef kebab with grilled vegetables", 70),
                ("Zibdiyit Gambari", "Spicy Gazan shrimp clay-pot stew", 60),
            ]),
        ],
        "reviews": [
            ("Khaled Nasser", 5, "The seafood here is unbeatable. Fresh and full of flavor."),
            ("Huda Saleh", 4, "Great grilled meats, generous portions, will come back."),
        ],
    },
    {
        "name": "Jerusalem Garden Cafe",
        "city": "Jerusalem",
        "category": "cafe",
        "tags": ["Cafe", "Breakfast", "Organic"],
        "is_open": False,
        "description": (
            "A peaceful courtyard cafe in the heart of Jerusalem, serving "
            "organic breakfasts, fresh juices, and specialty coffee in a "
            "garden setting surrounded by olive trees."
        ),
        "address": "Old City, Jerusalem",
        "open_time": "08:00", "close_time": "18:00",
        "cover_image_url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1200&q=80",
        "menu": [
            ("Breakfast", [
                ("Palestinian Breakfast Platter", "Labneh, olive oil, za'atar, olives, fresh vegetables and bread", 35),
                ("Shakshuka", "Eggs poached in spiced tomato sauce, served with fresh bread", 28),
            ]),
        ],
        "reviews": [
            ("Layla Hassan", 5, "Beautiful garden setting and the breakfast platter is generous and fresh."),
            ("Nadia Hammad", 5, "My favorite spot for weekend brunch. So peaceful."),
        ],
    },
    {
        "name": "Nablus Sweets Palace",
        "city": "Nablus",
        "category": "sweets",
        "tags": ["Kunafa", "Sweets", "Desserts"],
        "is_open": True,
        "description": (
            "Home of the original Nabulsi kunafa, this sweets palace has "
            "been perfecting traditional Palestinian desserts for "
            "generations using authentic Nablus cheese and pure syrup."
        ),
        "address": "Old City, Nablus",
        "open_time": "09:00", "close_time": "23:00",
        "cover_image_url": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=1200&q=80",
        "menu": [
            ("Desserts", [
                ("Kunafa Nabulsiyeh", "The original Nablus-style cheese kunafa with crispy semolina topping", 25),
                ("Baklava Assortment", "Mixed pistachio and walnut baklava selection", 30),
            ]),
        ],
        "reviews": [
            ("Omar Khalil", 5, "The best kunafa in all of Palestine, hands down."),
            ("Sara Al-Ahmad", 5, "Worth the trip to Nablus just for this kunafa."),
            ("Khaled Nasser", 4, "Sweet, rich, and authentic. A must-visit."),
        ],
    },
    {
        "name": "Bethlehem Terrace",
        "city": "Bethlehem",
        "category": "mediterranean",
        "tags": ["Mediterranean", "Seafood", "View"],
        "is_open": True,
        "description": (
            "Perched on a hillside terrace with sweeping views over "
            "Bethlehem, this restaurant blends Mediterranean classics with "
            "Palestinian hospitality and fresh seasonal ingredients."
        ),
        "address": "Manger Street, Bethlehem",
        "open_time": "11:00", "close_time": "22:30",
        "cover_image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80",
        "menu": [
            ("Mains", [
                ("Grilled Sea Bass", "Whole grilled sea bass with lemon, herbs and olive oil", 75),
                ("Mezze Platter", "Hummus, mutabbal, tabbouleh, fattoush and warm pita", 40),
            ]),
        ],
        "reviews": [
            ("Nadia Hammad", 5, "Incredible view and the mezze platter is huge and delicious."),
            ("Huda Saleh", 4, "Lovely terrace dining, perfect for sunset."),
        ],
    },
    {
        "name": "Jericho Palm",
        "city": "Jericho",
        "category": "traditional",
        "tags": ["Traditional", "Outdoor", "Family"],
        "is_open": False,
        "description": (
            "Set among the palm groves of Jericho, this family-run "
            "restaurant serves hearty traditional dishes in a shaded "
            "outdoor courtyard, perfect for large family gatherings."
        ),
        "address": "Ein As-Sultan, Jericho",
        "open_time": "12:00", "close_time": "22:00",
        "cover_image_url": "https://images.unsplash.com/photo-1424847651672-bf20a4b0982b?w=1200&q=80",
        "menu": [
            ("Mains", [
                ("Mansaf", "Traditional Jordanian-style mansaf with jameed yogurt sauce", 60),
                ("Freekeh with Chicken", "Smoked green wheat cooked with tender chicken pieces", 42),
            ]),
        ],
        "reviews": [
            ("Khaled Nasser", 4, "Great outdoor seating under the palms, very relaxing."),
            ("Layla Hassan", 5, "Generous portions and warm hospitality, perfect for families."),
        ],
    },
]

REVIEWER_EMAILS = {
    "Layla Hassan": "layla.hassan@example.com",
    "Omar Khalil": "omar.khalil@example.com",
    "Sara Al-Ahmad": "sara.alahmad@example.com",
    "Khaled Nasser": "khaled.nasser@example.com",
    "Huda Saleh": "huda.saleh@example.com",
    "Nadia Hammad": "nadia.hammad@example.com",
}


class Command(BaseCommand):
    help = "Seed the database with restaurants, menus and reviews matching the Figma design."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing restaurants/cities/tags/reviews before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing restaurant data...")
            Review.objects.all().delete()
            MenuItem.objects.all().delete()
            MenuCategory.objects.all().delete()
            Restaurant.objects.all().delete()
            CuisineTag.objects.all().delete()
            City.objects.all().delete()

        # ---- Cities ----
        city_objs = {}
        for name in CITIES:
            city, _ = City.objects.get_or_create(name=name)
            city_objs[name] = city
        self.stdout.write(self.style.SUCCESS(f"Cities ready: {len(city_objs)}"))

        # ---- Tags ----
        tag_objs = {}
        for name in TAGS:
            tag, _ = CuisineTag.objects.get_or_create(name=name)
            tag_objs[name] = tag
        self.stdout.write(self.style.SUCCESS(f"Tags ready: {len(tag_objs)}"))

        # ---- Reviewer users (plain "user" role) ----
        reviewer_objs = {}
        for display_name, email in REVIEWER_EMAILS.items():
            first, last = (display_name.split(" ", 1) + [""])[:2]
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "role": User.Role.USER,
                    "is_active": True,
                },
            )
            if created:
                user.set_password("SeedUser@2026")
                user.save(update_fields=["password"])
            reviewer_objs[display_name] = user
        self.stdout.write(self.style.SUCCESS(f"Reviewer users ready: {len(reviewer_objs)}"))

        # ---- Restaurants ----
        created_count = 0
        for data in RESTAURANTS:
            restaurant, created = Restaurant.objects.update_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "category": data["category"],
                    "city": city_objs[data["city"]],
                    "address": data["address"],
                    "working_hours_open": datetime.datetime.strptime(data["open_time"], "%H:%M").time(),
                    "working_hours_close": datetime.datetime.strptime(data["close_time"], "%H:%M").time(),
                    "cover_image_url": data["cover_image_url"],
                    "is_open": data["is_open"],
                },
            )
            restaurant.tags.set([tag_objs[t] for t in data["tags"]])

            # Menu
            restaurant.menu_categories.all().delete()
            for order, (cat_name, items) in enumerate(data["menu"], start=1):
                category = MenuCategory.objects.create(
                    restaurant=restaurant, name=cat_name, order=order
                )
                for item_name, item_desc, price in items:
                    MenuItem.objects.create(
                        category=category,
                        name=item_name,
                        description=item_desc,
                        price=price,
                    )

            # Reviews
            for reviewer_name, rating, comment in data["reviews"]:
                Review.objects.update_or_create(
                    restaurant=restaurant,
                    user=reviewer_objs[reviewer_name],
                    defaults={"rating": rating, "comment": comment},
                )

            created_count += 1
            status = "created" if created else "updated"
            self.stdout.write(f"  {status}: {restaurant.name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created_count} restaurants seeded with menus and reviews."
        ))