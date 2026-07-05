"""Add homepage Arabic translations to django.po."""

import polib
from pathlib import Path

INDEX_TRANSLATIONS = {
    "Discover the Best Restaurants in Palestine": "اكتشف أفضل المطاعم في فلسطين",
    "Palestine's #1 Food Platform": "منصة الطعام الأولى في فلسطين",
    "Discover the Best": "اكتشف أفضل",
    "Restaurants": "المطاعم",
    "in Palestine": "في فلسطين",
    "Explore menus, reviews, ratings, and our AI Assistant — all in one place.": (
        "استكشف القوائم والتقييمات ومساعد الذكاء الاصطناعي — كل شيء في مكان واحد."
    ),
    "Search restaurants, cuisines, cities...": "ابحث عن مطاعم، مأكولات، مدن...",
    "Search restaurants, cuisines, cities": "ابحث عن مطاعم، مأكولات، مدن",
    "Search": "بحث",
    "Explore Restaurants": "استكشف المطاعم",
    "Ask AI Assistant": "اسأل المساعد الذكي",
    "Platform statistics": "إحصائيات المنصة",
    "Happy Users": "مستخدم سعيد",
    "Top Rated": "الأعلى تقييماً",
    "Features": "المميزات",
    "Everything You Need": "كل ما تحتاجه",
    "A complete platform for discovering, reviewing, and reserving the best dining in Palestine.": (
        "منصة متكاملة لاكتشاف أفضل المطاعم الفلسطينية ومراجعتها وحجزها."
    ),
    "Describe your craving and our AI finds the perfect match instantly.": (
        "صف ما تشتهيه وسيجد ذكاؤنا الاصطناعي التطابق المثالي على الفور."
    ),
    "Interactive Map": "خريطة تفاعلية",
    "Discover restaurants near you on a live, interactive map.": (
        "اكتشف المطاعم القريبة منك على خريطة حية وتفاعلية."
    ),
    "Reviews & Ratings": "مراجعات وتقييمات",
    "Honest reviews from a trusted Palestinian food community.": (
        "مراجعات صادقة من مجتمع طعام فلسطيني موثوق."
    ),
    "Wishlist": "قائمة المفضلة",
    "Save your favourite restaurants for future visits.": "احفظ مطاعمك المفضلة لزيارات مستقبلية.",
    "Try it": "جرّبها",
    "Open Map": "افتح الخريطة",
    "Read Reviews": "اقرأ التقييمات",
    "View Saved": "عرض المحفوظات",
    "Process": "كيف يعمل",
    "How It Works": "كيف يعمل التطبيق",
    "Get started and find your next favourite restaurant in minutes.": (
        "ابدأ واعثر على مطعمك المفضل القادم في دقائق."
    ),
    "Register in under a minute, for free.": "سجّل في أقل من دقيقة، مجاناً.",
    "Browse hundreds of curated options.": "تصفح مئات الخيارات المنتقاة.",
    "Get hyper-personalised suggestions.": "احصل على اقتراحات مخصصة لك.",
    "Leave a Review": "اترك تقييماً",
    "Share your experience with the community.": "شارك تجربتك مع المجتمع.",
    "Handpicked": "مختارة بعناية",
    "Top Restaurants": "أفضل المطاعم",
    "Highest-rated picks across Palestine": "أعلى التقييمات في جميع أنحاء فلسطين",
    "View All": "عرض الكل",
    "View Restaurant": "عرض المطعم",
    "Open": "مفتوح",
    "Ready to Explore?": "مستعد للاستكشاف؟",
    "Join 1000+ food lovers discovering Palestine's best restaurants every day.": (
        "انضم إلى أكثر من 1000 محب للطعام يكتشفون أفضل مطاعم فلسطين كل يوم."
    ),
    "Palestine's leading restaurant discovery and review platform. Find exceptional dining across every city.": (
        "منصة فلسطين الرائدة لاكتشاف المطاعم وتقييمها. اعثر على أرقى تجارب الطعام في كل مدينة."
    ),
    "Platform": "المنصة",
    "Company": "الشركة",
    "About Us": "من نحن",
    "Contact": "تواصل معنا",
    "Privacy Policy": "سياسة الخصوصية",
    "Terms of Service": "شروط الخدمة",
    "© 2026 Yumm. Made with love for Palestine 🇵🇸": "© 2026 Yumm. صُنع بحب لفلسطين 🇵🇸",
}

po_path = Path(__file__).resolve().parent.parent / "locale" / "ar" / "LC_MESSAGES" / "django.po"
po = polib.pofile(str(po_path))
existing = {e.msgid for e in po}
added = 0
for msgid, msgstr in INDEX_TRANSLATIONS.items():
    if msgid in existing:
        entry = po.find(msgid)
        if entry and not entry.msgstr:
            entry.msgstr = msgstr
            added += 1
    else:
        po.append(polib.POEntry(msgid=msgid, msgstr=msgstr))
        added += 1
po.save(str(po_path))
po.save_as_mofile(str(po_path.with_suffix(".mo")))
print(f"updated po, added/updated {added}, total {len(po)}")
