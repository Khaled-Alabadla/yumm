"""Seed demo restaurants for public pages (DEBUG / development)."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from restaurants.constants import TAG_NAME_AR
from restaurants.menu_images import attach_menu_item_image
from restaurants.models import (
    MenuCategory,
    MenuItem,
    Restaurant,
    RestaurantCategory,
    Tag,
)
from reviews.models import Review


DEMO_RESTAURANTS = [
    {
        "name_en": "Al-Kanaan",
        "name_ar": "الكنعان",
        "city": Restaurant.City.RAMALLAH,
        "category": "Traditional Palestinian",
        "category_ar": "مأكولات فلسطينية تقليدية",
        "lat": "31.903800",
        "lng": "35.203400",
        "address_en": "Al-Masyoun, Ramallah",
        "address_ar": "الماصيون، رام الله",
        "description_en": (
            "Since 1987, Al-Kanaan has been serving authentic Palestinian "
            "dishes in a warm family atmosphere."
        ),
        "description_ar": "منذ 1987، يقدّم الكنعان أطباقاً فلسطينية أصيلة في أجواء عائلية دافئة.",
        "hours": "12:00 - 23:00",
        "price_range": 2,
        "tags": ["Mansaf", "Family", "Musakhan"],
        "menu": [
            ("Musakhan", "مسخن", "Roasted chicken on taboon bread with sumac onions.", "دجاج مشوي على خبز الطابون مع بصل السماق.", "45.00"),
            ("Mansaf", "منسف", "Lamb in jameed sauce on saffron rice.", "لحم ضأن بصلصة جميد على أرز بالزعفران.", "65.00"),
            ("Maqluba", "مقلوبة", "Upside-down rice with chicken and vegetables.", "أرز مقلوب مع دجاج وخضار.", "55.00"),
        ],
        "reviews": [(5, "Best musakhan in Ramallah!"), (5, "Authentic and delicious.")],
    },
    {
        "name_en": "Gaza Grill House",
        "name_ar": "بيت مشاوي غزة",
        "city": Restaurant.City.GAZA,
        "category": "Grills & BBQ",
        "category_ar": "مشاوي وشواء",
        "lat": "31.501700",
        "lng": "34.466700",
        "address_en": "Omar Mukhtar St, Gaza",
        "address_ar": "شارع عمر المختار، غزة",
        "description_en": "Premium charcoal grills and fresh seafood by the sea.",
        "description_ar": "مشاوي فاخرة على الفحم ومأكولات بحرية طازجة.",
        "hours": "11:00 - 00:00",
        "price_range": 2,
        "tags": ["Grills", "BBQ", "Seafood"],
        "menu": [
            ("Mixed Grill Platter", "طبق مشاوي مشكل", "Lamb, chicken, and kofta on charcoal.", "لحم ودجاج وكفتة مشوية على الفحم.", "85.00"),
            ("Grilled Sea Bream", "سمك دنيس مشوي", "Whole fish with lemon and herbs.", "سمك دنيس كامل مشوي مع ليمون وأعشاب.", "70.00"),
        ],
        "reviews": [(5, "Real fire-grilled flavour!"), (4, "Great portions and friendly staff.")],
    },
    {
        "name_en": "Jerusalem Garden Cafe",
        "name_ar": "مقهى حديقة القدس",
        "city": Restaurant.City.JERUSALEM,
        "category": "Cafe & Breakfast",
        "category_ar": "مقهى وفطور",
        "lat": "31.768300",
        "lng": "35.213700",
        "address_en": "Salah Ed-Din St, Jerusalem",
        "address_ar": "شارع صلاح الدين، القدس",
        "description_en": "Organic breakfast and specialty coffee in a peaceful garden setting.",
        "description_ar": "فطور عضوي وقهوة مختصة في حديقة هادئة.",
        "hours": "07:00 - 16:00",
        "price_range": 1,
        "tags": ["Cafe", "Breakfast", "Organic"],
        "menu": [
            ("Garden Breakfast", "فطور الحديقة", "Eggs, labneh, olives, and fresh bread.", "بيض، لبنة، زيتون، وخبز طازج.", "38.00"),
            ("Shakshuka", "شكشوكة", "Poached eggs in spiced tomato sauce.", "بيض مسلوق في صلصة طماطم متبلة.", "32.00"),
        ],
        "reviews": [(5, "Beautiful quiet atmosphere."), (5, "Best breakfast in Jerusalem.")],
    },
    {
        "name_en": "Nablus Sweets House",
        "name_ar": "بيت حلويات نابلس",
        "city": Restaurant.City.NABLUS,
        "category": "Sweets",
        "category_ar": "حلويات",
        "lat": "32.221100",
        "lng": "35.254400",
        "address_en": "Old City, Nablus",
        "address_ar": "البلدة القديمة، نابلس",
        "description_en": "Famous knafeh and traditional Palestinian desserts since 1960.",
        "description_ar": "كنافة مشهورة وحلويات فلسطينية تقليدية منذ 1960.",
        "hours": "09:00 - 22:00",
        "price_range": 1,
        "tags": ["Sweets", "Knafeh", "Family"],
        "menu": [
            ("Knafeh Nabulsiyeh", "كنافة نابلسية", "Warm cheese knafeh with syrup.", "كنافة جبنة دافئة مع القطر.", "18.00"),
            ("Ma'amoul Box", "علبة معمول", "Assorted date and nut pastries.", "معمول مشكل بالتمر والمكسرات.", "25.00"),
        ],
        "reviews": [(5, "The knafeh melts in your mouth!"), (4, "A must-visit in Nablus.")],
    },
    {
        "name_en": "Bethlehem Zaatar Oven",
        "name_ar": "فرن زعتر بيت لحم",
        "city": Restaurant.City.BETHLEHEM,
        "category": "Traditional Palestinian",
        "category_ar": "مأكولات فلسطينية تقليدية",
        "lat": "31.705400",
        "lng": "35.202400",
        "address_en": "Manger Square area, Bethlehem",
        "address_ar": "منطقة ساحة المهد، بيت لحم",
        "description_en": "Wood-fired taboon bread and classic Palestinian breakfast.",
        "description_ar": "خبز طابون على الحطب وفطور فلسطيني تقليدي.",
        "hours": "06:00 - 14:00",
        "price_range": 1,
        "tags": ["Breakfast", "Family", "Organic"],
        "menu": [
            ("Zaatar Manakish", "مناقيش زعتر", "Fresh taboon bread with olive oil and zaatar.", "خبز طابون طازج بزيت الزيتون والزعتر.", "12.00"),
            ("Labneh Plate", "طبق لبنة", "Creamy labneh with olive oil.", "لبنة كريمية مع زيت الزيتون.", "15.00"),
        ],
        "reviews": [(5, "Fresh from the oven every morning."), (5, "Simple and perfect.")],
    },
    {
        "name_en": "Jericho Dates & Grill",
        "name_ar": "تمور ومشاوي أريحا",
        "city": Restaurant.City.JERICHO,
        "category": "Grills & BBQ",
        "category_ar": "مشاوي وشواء",
        "lat": "31.866700",
        "lng": "35.450000",
        "address_en": "Jericho city centre",
        "address_ar": "وسط مدينة أريحا",
        "description_en": "Local dates, grills, and Jordan Valley specialties.",
        "description_ar": "تمور محلية ومشاوي وأطباق منخفضة البحر.",
        "hours": "10:00 - 22:00",
        "price_range": 2,
        "tags": ["Grills", "BBQ", "Family"],
        "menu": [
            ("Date Lamb Tagine", "طاجن لحم بالتمر", "Slow-cooked lamb with Jericho dates.", "لحم مطهو ببطء مع تمر أريحا.", "58.00"),
            ("Mixed Mezze", "مقبلات مشكلة", "Hummus, baba ghanoush, and salads.", "حمص، بابا غنوج، وسلطات.", "35.00"),
        ],
        "reviews": [(4, "Unique date dishes!"), (5, "Lovely outdoor seating.")],
    },
    {
        "name_en": "Al-Sham Kitchen",
        "name_ar": "مطبخ الشام",
        "city": Restaurant.City.RAMALLAH,
        "category": "Oriental",
        "category_ar": "أكل شرقي",
        "category_order": 4,
        "lat": "31.900500",
        "lng": "35.198200",
        "address_en": "Downtown Ramallah",
        "address_ar": "وسط رام الله",
        "description_en": "Classic Levantine mezze, hummus, falafel, and fresh tabbouleh.",
        "description_ar": "مقبلات شامية، حمص، فلافل، وتبولة طازجة.",
        "hours": "10:00 - 23:00",
        "price_range": 2,
        "tags": ["Family", "Organic"],
        "menu": [
            ("Mixed Mezze Platter", "طبق مقبلات مشكل", "Hummus, mutabal, tabbouleh, and pickles.", "حمص، متبل، تبولة، ومخللات.", "42.00"),
            ("Shawarma Plate", "طبق شاورما", "Chicken shawarma with garlic sauce and fries.", "شاورما دجاج مع ثوم وبطاطا.", "38.00"),
        ],
        "reviews": [(5, "Authentic Levantine flavours."), (4, "Great hummus and warm bread.")],
    },
    {
        "name_en": "Hebron Heritage Kitchen",
        "name_ar": "مطبخ تراث الخليل",
        "city": Restaurant.City.HEBRON,
        "category": "Traditional Palestinian",
        "category_ar": "مأكولات فلسطينية تقليدية",
        "category_order": 1,
        "lat": "31.532600",
        "lng": "35.099800",
        "address_en": "Old City, Hebron",
        "address_ar": "البلدة القديمة، الخليل",
        "description_en": "Hebron-style mansaf, maftoul, and slow-cooked family recipes.",
        "description_ar": "منسف على طريقة الخليل، مفتول، ووصفات عائلية مطهية ببطء.",
        "hours": "12:00 - 22:00",
        "price_range": 2,
        "tags": ["Mansaf", "Family"],
        "menu": [
            ("Hebron Mansaf", "منسف الخليل", "Lamb mansaf with jameed and shrak bread.", "منسف لحم بجميد وخبز شراك.", "68.00"),
            ("Maftoul with Chicken", "مفتول بالدجاج", "Hand-rolled couscous with chicken and chickpeas.", "مفتول يدوي مع دجاج وحمص.", "52.00"),
        ],
        "reviews": [(5, "The mansaf is incredible."), (5, "True Hebron hospitality.")],
    },
    {
        "name_en": "Gaza Mediterranean Blue",
        "name_ar": "أزرق المتوسط — غزة",
        "city": Restaurant.City.GAZA,
        "category": "Mediterranean",
        "category_ar": "متوسطي",
        "category_order": 6,
        "lat": "31.513500",
        "lng": "34.458500",
        "address_en": "Gaza seafront",
        "address_ar": "الواجهة البحرية، غزة",
        "description_en": "Fresh Mediterranean seafood, grilled fish, and coastal salads.",
        "description_ar": "مأكولات بحرية متوسطية طازجة، أسماك مشوية، وسلطات ساحلية.",
        "hours": "11:00 - 23:30",
        "price_range": 3,
        "tags": ["Seafood", "Family"],
        "menu": [
            ("Grilled Sea Bass", "قاروس مشوي", "Whole sea bass with lemon and herbs.", "قاروس كامل مشوي مع ليمون وأعشاب.", "75.00"),
            ("Seafood Paella", "أرز بحري", "Rice with shrimp, calamari, and saffron.", "أرز مع روبيان وحبار وزعفران.", "90.00"),
        ],
        "reviews": [(5, "Fresh catch every day!"), (4, "Beautiful sea view.")],
    },
    {
        "name_en": "Ramallah Sweet Palace",
        "name_ar": "قصر الحلويات — رام الله",
        "city": Restaurant.City.RAMALLAH,
        "category": "Sweets",
        "category_ar": "حلويات",
        "category_order": 3,
        "lat": "31.907200",
        "lng": "35.210100",
        "address_en": "Al-Tireh, Ramallah",
        "address_ar": "حي الطيرة، رام الله",
        "description_en": "Knafeh, baklava, maamoul, and Arabic ice cream.",
        "description_ar": "كنافة، بقلاوة، معمول، وآيس كريم عربي.",
        "hours": "09:00 - 23:00",
        "price_range": 1,
        "tags": ["Sweets", "Knafeh", "Family"],
        "menu": [
            ("Knafeh with Cream", "كنافة بالقشطة", "Warm knafeh topped with clotted cream.", "كنافة دافئة مع قشطة.", "22.00"),
            ("Baklava Assortment", "تشكيلة بقلاوة", "Pistachio and walnut baklava selection.", "تشكيلة بقلاوة بالفستق والجوز.", "28.00"),
        ],
        "reviews": [(5, "Best sweets in Ramallah!"), (5, "Knafeh is perfect.")],
    },
    {
        "name_en": "Jerusalem Shawarma Express",
        "name_ar": "شاورما القدس السريعة",
        "city": Restaurant.City.JERUSALEM,
        "category": "Oriental",
        "category_ar": "أكل شرقي",
        "category_order": 4,
        "lat": "31.781000",
        "lng": "35.229500",
        "address_en": "Damascus Gate area, Jerusalem",
        "address_ar": "منطقة باب العامود، القدس",
        "description_en": "Quick shawarma wraps, falafel sandwiches, and fresh juices.",
        "description_ar": "ساندويچ شاورما سريعة، فلافل، وعصائر طازجة.",
        "hours": "08:00 - 02:00",
        "price_range": 1,
        "tags": ["Grills", "Family"],
        "menu": [
            ("Chicken Shawarma Wrap", "ساندويچ شاورما دجاج", "Marinated chicken with tahini and pickles.", "دجاج متبل مع طحينة ومخللات.", "25.00"),
            ("Falafel Sandwich", "ساندويچ فلافل", "Crispy falafel with hummus and salad.", "فلافل مقرمش مع حمص وسلطة.", "18.00"),
        ],
        "reviews": [(4, "Fast and tasty."), (5, "Open late — perfect after a walk.")],
    },
]


CATEGORY_ORDER = {
    "Traditional Palestinian": 1,
    "Grills & BBQ": 2,
    "Sweets": 3,
    "Oriental": 4,
    "Cafe & Breakfast": 5,
    "Mediterranean": 6,
}


class Command(BaseCommand):
    help = "Create demo active restaurants with menus, tags, and reviews."

    def handle(self, *args, **options):
        User = get_user_model()
        reviewer, _ = User.objects.get_or_create(
            email="demo.reviewer@yumm.ps",
            defaults={
                "first_name": "Demo",
                "last_name": "Reviewer",
                "role": User.Role.USER,
                "is_approved": True,
            },
        )

        created_count = 0
        for data in DEMO_RESTAURANTS:
            order = data.get("category_order", CATEGORY_ORDER.get(data["category"], 0))
            category, _ = RestaurantCategory.objects.get_or_create(
                name_en=data["category"],
                defaults={"name_ar": data["category_ar"], "order": order},
            )
            if category.order != order or category.name_ar != data["category_ar"]:
                category.order = order
                category.name_ar = data["category_ar"]
                category.save(update_fields=["order", "name_ar"])

            restaurant, created = Restaurant.objects.get_or_create(
                name_en=data["name_en"],
                defaults={
                    "name_ar": data["name_ar"],
                    "city": data["city"],
                    "category": category,
                    "address_en": data["address_en"],
                    "address_ar": data["address_ar"],
                    "description_en": data["description_en"],
                    "description_ar": data["description_ar"],
                    "working_hours_en": data["hours"],
                    "working_hours_ar": data["hours"],
                    "latitude": Decimal(data["lat"]),
                    "longitude": Decimal(data["lng"]),
                    "price_range": data["price_range"],
                    "is_open": True,
                    "status": Restaurant.Status.ACTIVE,
                },
            )

            if not created:
                updates = {
                    "name_ar": data["name_ar"],
                    "city": data["city"],
                    "category": category,
                    "address_en": data["address_en"],
                    "address_ar": data["address_ar"],
                    "description_en": data["description_en"],
                    "description_ar": data["description_ar"],
                    "working_hours_en": data["hours"],
                    "working_hours_ar": data["hours"],
                    "latitude": Decimal(data["lat"]),
                    "longitude": Decimal(data["lng"]),
                    "price_range": data["price_range"],
                    "status": Restaurant.Status.ACTIVE,
                }
                changed = []
                for field, value in updates.items():
                    if getattr(restaurant, field) != value:
                        setattr(restaurant, field, value)
                        changed.append(field)
                if changed:
                    restaurant.save(update_fields=changed)

            tag_objs = []
            for tag_name in data["tags"]:
                name_ar = TAG_NAME_AR.get(tag_name, tag_name)
                tag, _ = Tag.objects.get_or_create(
                    name_en=tag_name,
                    defaults={"name_ar": name_ar},
                )
                if tag.name_ar != name_ar:
                    tag.name_ar = name_ar
                    tag.save(update_fields=["name_ar"])
                tag_objs.append(tag)
            restaurant.tags.set(tag_objs)

            menu_cat, _ = MenuCategory.objects.get_or_create(
                restaurant=restaurant,
                name_en="Main Dishes",
                defaults={"name_ar": "الأطباق الرئيسية", "order": 0},
            )

            for order, menu_entry in enumerate(data["menu"]):
                name_en, name_ar, desc_en, desc_ar, price = menu_entry
                item, _ = MenuItem.objects.get_or_create(
                    restaurant=restaurant,
                    name_en=name_en,
                    defaults={
                        "category": menu_cat,
                        "name_ar": name_ar,
                        "description_en": desc_en,
                        "description_ar": desc_ar,
                        "price": price,
                        "order": order,
                        "is_available": True,
                    },
                )
                updates = {}
                if item.name_ar != name_ar:
                    updates["name_ar"] = name_ar
                if item.description_en != desc_en:
                    updates["description_en"] = desc_en
                if item.description_ar != desc_ar:
                    updates["description_ar"] = desc_ar
                if updates:
                    for field, value in updates.items():
                        setattr(item, field, value)
                    item.save(update_fields=list(updates))
                attach_menu_item_image(item)

            for i, (rating, comment) in enumerate(data["reviews"]):
                Review.objects.get_or_create(
                    user=reviewer,
                    restaurant=restaurant,
                    defaults={
                        "rating": rating,
                        "comment": comment,
                        "is_visible": True,
                    },
                )

            if created:
                created_count += 1

        images_attached = 0
        for item in MenuItem.objects.filter(image=""):
            if attach_menu_item_image(item):
                images_attached += 1

        for tag in Tag.objects.all():
            name_ar = TAG_NAME_AR.get(tag.name_en)
            if name_ar and tag.name_ar != name_ar:
                tag.name_ar = name_ar
                tag.save(update_fields=["name_ar"])

        total = Restaurant.objects.filter(status=Restaurant.Status.ACTIVE).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {created_count} new restaurants. "
                f"Attached {images_attached} dish photos. "
                f"{total} active restaurants total.",
            )
        )
