/* ─────────────────────────────
Yumm — Main JavaScript
───────────────────────────── */

// Initialise Lucide icons
lucide.createIcons();

/* ─────────────────────────────
Theme (dark / light)
───────────────────────────── */
const html = document.documentElement;

function applyTheme(dark) {
    html.classList.toggle('dark', dark);
    document.getElementById('icon-moon').classList.toggle('hidden',  dark);
    document.getElementById('icon-sun') .classList.toggle('hidden', !dark);
    document.getElementById('theme-btn').setAttribute('aria-pressed', String(dark));
    localStorage.setItem('yumm-theme', dark ? 'dark' : 'light');
}

const savedTheme = localStorage.getItem('yumm-theme');
applyTheme(
    savedTheme === 'dark' ||
    (!savedTheme && window.matchMedia('(prefers-color-scheme:dark)').matches)
);

function toggleTheme() { applyTheme(!html.classList.contains('dark')); }

/* ─────────────────────────────
Live Clock
───────────────────────────── */
function updateClock() {
    const now = new Date();
    const t = document.getElementById('clock-time');
    const d = document.getElementById('clock-date');
    if (!t) return;
    t.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    d.textContent = now.toLocaleDateString([],  { weekday: 'short', month: 'short', day: 'numeric' });
}
updateClock();
setInterval(updateClock, 1000);

/* ─────────────────────────────
Translations
───────────────────────────── */
const translations = {
    en: {
        // Navbar
        'nav-home':          'Home',
        'nav-restaurants':   'Restaurants',
        'nav-ai':            'AI Assistant',
        'nav-login':         'Login',
        'nav-register':      'Register',
        // Hero
        'hero-badge':        "Palestine's #1 Food Platform",
        'hero-h1-line1':     'Discover the Best',
        'hero-h1-span':      'Restaurants',
        'hero-h1-line2':     'in Palestine',
        'hero-desc':         'Explore menus, reviews, ratings, reservations, and AI-powered recommendations — all in one place.',
        'hero-search-ph':    'Search restaurants, cuisines, cities...',
        'hero-search-btn':   'Search',
        'hero-cta1':         'Explore Restaurants',
        'hero-cta2':         'Ask AI Assistant',
        // Stats
        'stat-restaurants':  'Restaurants',
        'stat-reviews':      'Reviews',
        'stat-users':        'Happy Users',
        'stat-rated':        'Top Rated',
        // Features
        'feat-label':        'Features',
        'feat-h2':           'Everything You Need',
        'feat-desc':         "A complete platform for discovering, reviewing, and reserving the best dining in Palestine.",
        'feat1-title':       'AI Assistant',
        'feat1-desc':        'Describe your craving and our AI finds the perfect match instantly.',
        'feat2-title':       'Interactive Map',
        'feat2-desc':        'Discover restaurants near you on a live, interactive map.',
        'feat3-title':       'Reviews & Ratings',
        'feat3-desc':        'Honest reviews from a trusted Palestinian food community.',
        'feat4-title':       'Wishlist',
        'feat4-desc':        'Save your favourite restaurants for future visits.',
        // How it works
        'how-label':         'Process',
        'how-h2':            'How It Works',
        'how-desc':          'Get started and find your next favourite restaurant in minutes.',
        'step1-title':       'Create Account',
        'step1-desc':        'Register in under a minute, for free.',
        'step2-title':       'Explore Restaurants',
        'step2-desc':        'Browse hundreds of curated options.',
        'step3-title':       'Ask AI Assistant',
        'step3-desc':        'Get hyper-personalised suggestions.',
        'step4-title':       'Reserve or Order',
        'step4-desc':        'Book a table or request delivery.',
        'step5-title':       'Leave a Review',
        'step5-desc':        'Share your experience with the community.',
        // Restaurants section
        'rest-label':        'Handpicked',
        'rest-h2':           'Top Restaurants',
        'rest-desc':         "Highest-rated picks across Palestine",
        'rest-view-all':     'View All',
        'card-view-btn':     'View Restaurant',
        // CTA
        'cta-h2':            'Ready to Explore?',
        'cta-desc':          "Join 1000+ food lovers discovering Palestine's best restaurants every day.",
        'cta-btn':           'Create Free Account',
        // Footer
        'footer-desc':       "Palestine's leading restaurant discovery and reservation platform. Find exceptional dining across every city.",
        'footer-platform':   'Platform',
        'footer-company':    'Company',
        'footer-about':      'About Us',
        'footer-contact':    'Contact',
        'footer-privacy':    'Privacy Policy',
        'footer-terms':      'Terms of Service',
        'footer-copy':       '© 2024 Yumm. Made with love for Palestine 🇵🇸',
    },
    ar: {
        'nav-home':          'الرئيسية',
        'nav-restaurants':   'المطاعم',
        'nav-ai':            'مساعد الذكاء الاصطناعي',
        'nav-login':         'تسجيل الدخول',
        'nav-register':      'إنشاء حساب',
        'hero-badge':        'منصة الطعام الأولى في فلسطين',
        'hero-h1-line1':     'اكتشف أفضل',
        'hero-h1-span':      'المطاعم',
        'hero-h1-line2':     'في فلسطين',
        'hero-desc':         'استكشف القوائم والتقييمات والحجوزات وتوصيات الذكاء الاصطناعي — كل شيء في مكان واحد.',
        'hero-search-ph':    'ابحث عن مطاعم، مأكولات، مدن...',
        'hero-search-btn':   'بحث',
        'hero-cta1':         'استكشف المطاعم',
        'hero-cta2':         'اسأل المساعد الذكي',
        'stat-restaurants':  'مطعم',
        'stat-reviews':      'تقييم',
        'stat-users':        'مستخدم سعيد',
        'stat-rated':        'الأعلى تقييماً',
        'feat-label':        'المميزات',
        'feat-h2':           'كل ما تحتاجه',
        'feat-desc':         'منصة متكاملة لاكتشاف أفضل المطاعم الفلسطينية ومراجعتها وحجزها.',
        'feat1-title':       'المساعد الذكي',
        'feat1-desc':        'صف ما تشتهيه وسيجد ذكاؤنا الاصطناعي التطابق المثالي على الفور.',
        'feat2-title':       'خريطة تفاعلية',
        'feat2-desc':        'اكتشف المطاعم القريبة منك على خريطة حية وتفاعلية.',
        'feat3-title':       'مراجعات وتقييمات',
        'feat3-desc':        'مراجعات صادقة من مجتمع طعام فلسطيني موثوق.',
        'feat4-title':       'قائمة المفضلة',
        'feat4-desc':        'احفظ مطاعمك المفضلة لزيارات مستقبلية.',
        'how-label':         'كيف يعمل',
        'how-h2':            'كيف يعمل التطبيق',
        'how-desc':          'ابدأ واعثر على مطعمك المفضل القادم في دقائق.',
        'step1-title':       'إنشاء حساب',
        'step1-desc':        'سجّل في أقل من دقيقة، مجاناً.',
        'step2-title':       'استكشف المطاعم',
        'step2-desc':        'تصفح مئات الخيارات المنتقاة.',
        'step3-title':       'اسأل المساعد الذكي',
        'step3-desc':        'احصل على اقتراحات مخصصة لك.',
        'step4-title':       'احجز أو اطلب',
        'step4-desc':        'احجز طاولة أو اطلب التوصيل.',
        'step5-title':       'اترك تقييماً',
        'step5-desc':        'شارك تجربتك مع المجتمع.',
        'rest-label':        'مختارة بعناية',
        'rest-h2':           'أفضل المطاعم',
        'rest-desc':         'أعلى التقييمات في جميع أنحاء فلسطين',
        'rest-view-all':     'عرض الكل',
        'card-view-btn':     'عرض المطعم',
        'cta-h2':            'مستعد للاستكشاف؟',
        'cta-desc':          'انضم إلى أكثر من 1000 محب للطعام يكتشفون أفضل مطاعم فلسطين كل يوم.',
        'cta-btn':           'إنشاء حساب مجاني',
        'footer-desc':       'منصة فلسطين الرائدة لاكتشاف المطاعم وحجزها. اعثر على أرقى تجارب الطعام في كل مدينة.',
        'footer-platform':   'المنصة',
        'footer-company':    'الشركة',
        'footer-about':      'من نحن',
        'footer-contact':    'تواصل معنا',
        'footer-privacy':    'سياسة الخصوصية',
        'footer-terms':      'شروط الخدمة',
        'footer-copy':       '© 2024 Yumm. صُنع بحب لفلسطين 🇵🇸',
    },
    fr: {
        'nav-home':          'Accueil',
        'nav-restaurants':   'Restaurants',
        'nav-ai':            'Assistant IA',
        'nav-login':         'Connexion',
        'nav-register':      "S'inscrire",
        'hero-badge':        'Plateforme #1 en Palestine',
        'hero-h1-line1':     'Découvrez les Meilleurs',
        'hero-h1-span':      'Restaurants',
        'hero-h1-line2':     'en Palestine',
        'hero-desc':         'Explorez les menus, avis, notes, réservations et recommandations IA — tout en un seul endroit.',
        'hero-search-ph':    'Rechercher restaurants, cuisines, villes...',
        'hero-search-btn':   'Rechercher',
        'hero-cta1':         'Explorer les Restaurants',
        'hero-cta2':         "Demander à l'Assistant IA",
        'stat-restaurants':  'Restaurants',
        'stat-reviews':      'Avis',
        'stat-users':        'Utilisateurs Satisfaits',
        'stat-rated':        'Mieux Notés',
        'feat-label':        'Fonctionnalités',
        'feat-h2':           'Tout ce dont vous avez besoin',
        'feat-desc':         'Une plateforme complète pour découvrir, évaluer et réserver les meilleurs restaurants en Palestine.',
        'feat1-title':       'Assistant IA',
        'feat1-desc':        'Décrivez votre envie et notre IA trouve la correspondance parfaite instantanément.',
        'feat2-title':       'Carte Interactive',
        'feat2-desc':        'Découvrez les restaurants près de chez vous sur une carte interactive en direct.',
        'feat3-title':       'Avis & Notes',
        'feat3-desc':        "Avis honnêtes d'une communauté palestinienne de confiance.",
        'feat4-title':       'Liste de Souhaits',
        'feat4-desc':        'Sauvegardez vos restaurants préférés pour de futures visites.',
        'how-label':         'Processus',
        'how-h2':            'Comment ça marche',
        'how-desc':          'Commencez et trouvez votre prochain restaurant préféré en minutes.',
        'step1-title':       'Créer un Compte',
        'step1-desc':        "Inscrivez-vous en moins d'une minute, gratuitement.",
        'step2-title':       'Explorer les Restaurants',
        'step2-desc':        "Parcourez des centaines d'options sélectionnées.",
        'step3-title':       "Demander à l'Assistant IA",
        'step3-desc':        'Obtenez des suggestions hyper-personnalisées.',
        'step4-title':       'Réserver ou Commander',
        'step4-desc':        'Réservez une table ou demandez une livraison.',
        'step5-title':       'Laisser un Avis',
        'step5-desc':        'Partagez votre expérience avec la communauté.',
        'rest-label':        'Sélection',
        'rest-h2':           'Meilleurs Restaurants',
        'rest-desc':         'Les choix les mieux notés en Palestine',
        'rest-view-all':     'Voir Tout',
        'card-view-btn':     'Voir le Restaurant',
        'cta-h2':            'Prêt à Explorer?',
        'cta-desc':          "Rejoignez plus de 1000 amateurs de gastronomie qui découvrent les meilleurs restaurants de Palestine chaque jour.",
        'cta-btn':           'Créer un Compte Gratuit',
        'footer-desc':       "La principale plateforme de découverte et de réservation de restaurants en Palestine.",
        'footer-platform':   'Plateforme',
        'footer-company':    'Société',
        'footer-about':      'À Propos',
        'footer-contact':    'Contact',
        'footer-privacy':    'Politique de Confidentialité',
        'footer-terms':      "Conditions d'Utilisation",
        'footer-copy':       '© 2024 Yumm. Fait avec amour pour la Palestine 🇵🇸',
    },
    de: {
        'nav-home':          'Startseite',
        'nav-restaurants':   'Restaurants',
        'nav-ai':            'KI-Assistent',
        'nav-login':         'Anmelden',
        'nav-register':      'Registrieren',
        'hero-badge':        'Palästinas #1 Food-Plattform',
        'hero-h1-line1':     'Entdecken Sie die Besten',
        'hero-h1-span':      'Restaurants',
        'hero-h1-line2':     'in Palästina',
        'hero-desc':         'Erkunden Sie Menüs, Bewertungen, Reservierungen und KI-Empfehlungen — alles an einem Ort.',
        'hero-search-ph':    'Restaurants, Küchen, Städte suchen...',
        'hero-search-btn':   'Suchen',
        'hero-cta1':         'Restaurants Erkunden',
        'hero-cta2':         'KI-Assistent Fragen',
        'stat-restaurants':  'Restaurants',
        'stat-reviews':      'Bewertungen',
        'stat-users':        'Zufriedene Nutzer',
        'stat-rated':        'Top Bewertet',
        'feat-label':        'Funktionen',
        'feat-h2':           'Alles was Sie brauchen',
        'feat-desc':         'Eine vollständige Plattform zum Entdecken, Bewerten und Reservieren.',
        'feat1-title':       'KI-Assistent',
        'feat1-desc':        'Beschreiben Sie Ihren Hunger und unsere KI findet sofort die perfekte Übereinstimmung.',
        'feat2-title':       'Interaktive Karte',
        'feat2-desc':        'Entdecken Sie Restaurants in Ihrer Nähe auf einer Live-Karte.',
        'feat3-title':       'Bewertungen',
        'feat3-desc':        'Ehrliche Bewertungen von einer vertrauenswürdigen Gemeinschaft.',
        'feat4-title':       'Wunschliste',
        'feat4-desc':        'Speichern Sie Ihre Lieblingsrestaurants für zukünftige Besuche.',
        'how-label':         'Prozess',
        'how-h2':            'Wie es funktioniert',
        'how-desc':          'Starten Sie und finden Sie Ihr nächstes Lieblingsrestaurant in Minuten.',
        'step1-title':       'Konto Erstellen',
        'step1-desc':        'Registrieren Sie sich in weniger als einer Minute, kostenlos.',
        'step2-title':       'Restaurants Erkunden',
        'step2-desc':        'Durchsuchen Sie Hunderte von kuratierten Optionen.',
        'step3-title':       'KI-Assistent Fragen',
        'step3-desc':        'Erhalten Sie hyper-personalisierte Vorschläge.',
        'step4-title':       'Reservieren oder Bestellen',
        'step4-desc':        'Tisch buchen oder Lieferung anfordern.',
        'step5-title':       'Bewertung Hinterlassen',
        'step5-desc':        'Teilen Sie Ihre Erfahrung mit der Community.',
        'rest-label':        'Handverlesen',
        'rest-h2':           'Top Restaurants',
        'rest-desc':         'Die am besten bewerteten Restaurants in Palästina',
        'rest-view-all':     'Alle Ansehen',
        'card-view-btn':     'Restaurant Ansehen',
        'cta-h2':            'Bereit zu Erkunden?',
        'cta-desc':          'Schließen Sie sich über 1000 Essensliebhabern an, die täglich Palästinas beste Restaurants entdecken.',
        'cta-btn':           'Kostenloses Konto Erstellen',
        'footer-desc':       'Palästinas führende Plattform zur Entdeckung und Reservierung von Restaurants.',
        'footer-platform':   'Plattform',
        'footer-company':    'Unternehmen',
        'footer-about':      'Über Uns',
        'footer-contact':    'Kontakt',
        'footer-privacy':    'Datenschutzrichtlinie',
        'footer-terms':      'Nutzungsbedingungen',
        'footer-copy':       '© 2024 Yumm. Mit Liebe für Palästina gemacht 🇵🇸',
    },
    es: {
        'nav-home':          'Inicio',
        'nav-restaurants':   'Restaurantes',
        'nav-ai':            'Asistente IA',
        'nav-login':         'Iniciar Sesión',
        'nav-register':      'Registrarse',
        'hero-badge':        'Plataforma #1 de Palestina',
        'hero-h1-line1':     'Descubre los Mejores',
        'hero-h1-span':      'Restaurantes',
        'hero-h1-line2':     'en Palestina',
        'hero-desc':         'Explora menús, reseñas, calificaciones, reservas y recomendaciones de IA — todo en un solo lugar.',
        'hero-search-ph':    'Buscar restaurantes, cocinas, ciudades...',
        'hero-search-btn':   'Buscar',
        'hero-cta1':         'Explorar Restaurantes',
        'hero-cta2':         'Preguntar al Asistente IA',
        'stat-restaurants':  'Restaurantes',
        'stat-reviews':      'Reseñas',
        'stat-users':        'Usuarios Felices',
        'stat-rated':        'Mejor Valorados',
        'feat-label':        'Características',
        'feat-h2':           'Todo lo que Necesitas',
        'feat-desc':         'Una plataforma completa para descubrir, reseñar y reservar los mejores restaurantes en Palestina.',
        'feat1-title':       'Asistente IA',
        'feat1-desc':        'Describe tu antojo y nuestra IA encuentra la coincidencia perfecta al instante.',
        'feat2-title':       'Mapa Interactivo',
        'feat2-desc':        'Descubre restaurantes cerca de ti en un mapa interactivo en vivo.',
        'feat3-title':       'Reseñas y Calificaciones',
        'feat3-desc':        'Reseñas honestas de una comunidad palestina de confianza.',
        'feat4-title':       'Lista de Deseos',
        'feat4-desc':        'Guarda tus restaurantes favoritos para visitas futuras.',
        'how-label':         'Proceso',
        'how-h2':            'Cómo Funciona',
        'how-desc':          'Comienza y encuentra tu próximo restaurante favorito en minutos.',
        'step1-title':       'Crear Cuenta',
        'step1-desc':        'Regístrate en menos de un minuto, gratis.',
        'step2-title':       'Explorar Restaurantes',
        'step2-desc':        'Navega entre cientos de opciones seleccionadas.',
        'step3-title':       'Preguntar al Asistente IA',
        'step3-desc':        'Obtén sugerencias hiperpersonalizadas.',
        'step4-title':       'Reservar o Pedir',
        'step4-desc':        'Reserva una mesa o solicita entrega.',
        'step5-title':       'Dejar una Reseña',
        'step5-desc':        'Comparte tu experiencia con la comunidad.',
        'rest-label':        'Seleccionados',
        'rest-h2':           'Mejores Restaurantes',
        'rest-desc':         'Los más valorados en toda Palestina',
        'rest-view-all':     'Ver Todo',
        'card-view-btn':     'Ver Restaurante',
        'cta-h2':            '¿Listo para Explorar?',
        'cta-desc':          'Únete a más de 1000 amantes de la comida que descubren los mejores restaurantes de Palestina cada día.',
        'cta-btn':           'Crear Cuenta Gratuita',
        'footer-desc':       'La principal plataforma de descubrimiento y reserva de restaurantes de Palestina.',
        'footer-platform':   'Plataforma',
        'footer-company':    'Empresa',
        'footer-about':      'Sobre Nosotros',
        'footer-contact':    'Contacto',
        'footer-privacy':    'Política de Privacidad',
        'footer-terms':      'Términos de Servicio',
        'footer-copy':       '© 2024 Yumm. Hecho con amor por Palestina 🇵🇸',
    },
    tr: {
        'nav-home':          'Ana Sayfa',
        'nav-restaurants':   'Restoranlar',
        'nav-ai':            'Yapay Zeka Asistanı',
        'nav-login':         'Giriş Yap',
        'nav-register':      'Kayıt Ol',
        'hero-badge':        "Filistin'in #1 Yemek Platformu",
        'hero-h1-line1':     'En İyi',
        'hero-h1-span':      'Restoranları',
        'hero-h1-line2':     "Filistin'de Keşfet",
        'hero-desc':         'Menüleri, yorumları, puanları, rezervasyonları ve yapay zeka önerilerini keşfedin — hepsi bir arada.',
        'hero-search-ph':    'Restoran, mutfak, şehir ara...',
        'hero-search-btn':   'Ara',
        'hero-cta1':         'Restoranları Keşfet',
        'hero-cta2':         'Yapay Zeka Asistanına Sor',
        'stat-restaurants':  'Restoran',
        'stat-reviews':      'Yorum',
        'stat-users':        'Mutlu Kullanıcı',
        'stat-rated':        'En Yüksek Puan',
        'feat-label':        'Özellikler',
        'feat-h2':           'İhtiyacınız Olan Her Şey',
        'feat-desc':         "Filistin'deki en iyi restoranları keşfetmek, incelemek ve rezervasyon yapmak için tam bir platform.",
        'feat1-title':       'Yapay Zeka Asistanı',
        'feat1-desc':        'Canınızın ne çektiğini söyleyin, yapay zekamız anında mükemmel eşleşmeyi bulsun.',
        'feat2-title':       'Etkileşimli Harita',
        'feat2-desc':        'Yakınızdaki restoranları canlı, etkileşimli bir haritada keşfedin.',
        'feat3-title':       'Yorumlar ve Puanlar',
        'feat3-desc':        'Güvenilir Filistin yemek topluluğundan dürüst yorumlar.',
        'feat4-title':       'İstek Listesi',
        'feat4-desc':        'Favori restoranlarınızı gelecekteki ziyaretler için kaydedin.',
        'how-label':         'Süreç',
        'how-h2':            'Nasıl Çalışır',
        'how-desc':          'Başlayın ve dakikalar içinde bir sonraki favori restoranınızı bulun.',
        'step1-title':       'Hesap Oluştur',
        'step1-desc':        'Bir dakikadan kısa sürede ücretsiz kayıt olun.',
        'step2-title':       'Restoranları Keşfet',
        'step2-desc':        'Yüzlerce özenle seçilmiş seçeneğe göz atın.',
        'step3-title':       'Yapay Zeka Asistanına Sor',
        'step3-desc':        'Hiper-kişiselleştirilmiş öneriler alın.',
        'step4-title':       'Rezervasyon Yap veya Sipariş Ver',
        'step4-desc':        'Masa rezervasyonu yapın veya teslimat isteyin.',
        'step5-title':       'Yorum Bırak',
        'step5-desc':        'Deneyiminizi toplulukla paylaşın.',
        'rest-label':        'Özenle Seçilmiş',
        'rest-h2':           'En İyi Restoranlar',
        'rest-desc':         "Filistin genelinde en yüksek puanlı seçimler",
        'rest-view-all':     'Tümünü Gör',
        'card-view-btn':     'Restoranı Gör',
        'cta-h2':            'Keşfetmeye Hazır mısınız?',
        'cta-desc':          "Her gün Filistin'in en iyi restoranlarını keşfeden 1000'den fazla yemek tutkununa katılın.",
        'cta-btn':           'Ücretsiz Hesap Oluştur',
        'footer-desc':       "Filistin'in önde gelen restoran keşif ve rezervasyon platformu.",
        'footer-platform':   'Platform',
        'footer-company':    'Şirket',
        'footer-about':      'Hakkımızda',
        'footer-contact':    'İletişim',
        'footer-privacy':    'Gizlilik Politikası',
        'footer-terms':      'Hizmet Şartları',
        'footer-copy':       "© 2024 Yumm. Filistin için sevgiyle yapıldı 🇵🇸",
    },
    ru: {
        'nav-home':          'Главная',
        'nav-restaurants':   'Рестораны',
        'nav-ai':            'ИИ-Ассистент',
        'nav-login':         'Войти',
        'nav-register':      'Регистрация',
        'hero-badge':        'Платформа №1 в Палестине',
        'hero-h1-line1':     'Откройте Лучшие',
        'hero-h1-span':      'Рестораны',
        'hero-h1-line2':     'в Палестине',
        'hero-desc':         'Изучайте меню, отзывы, рейтинги, бронирования и рекомендации ИИ — всё в одном месте.',
        'hero-search-ph':    'Поиск ресторанов, кухонь, городов...',
        'hero-search-btn':   'Найти',
        'hero-cta1':         'Исследовать Рестораны',
        'hero-cta2':         'Спросить ИИ-Ассистента',
        'stat-restaurants':  'Ресторанов',
        'stat-reviews':      'Отзывов',
        'stat-users':        'Довольных Пользователей',
        'stat-rated':        'Топ Рейтинг',
        'feat-label':        'Возможности',
        'feat-h2':           'Всё что нужно',
        'feat-desc':         'Полная платформа для открытия, отзывов и бронирования лучших ресторанов Палестины.',
        'feat1-title':       'ИИ-Ассистент',
        'feat1-desc':        'Опишите своё желание и наш ИИ мгновенно найдёт идеальный вариант.',
        'feat2-title':       'Интерактивная Карта',
        'feat2-desc':        'Открывайте рестораны рядом с вами на живой интерактивной карте.',
        'feat3-title':       'Отзывы и Рейтинги',
        'feat3-desc':        'Честные отзывы от доверенного палестинского гастрономического сообщества.',
        'feat4-title':       'Список Желаний',
        'feat4-desc':        'Сохраняйте любимые рестораны для будущих визитов.',
        'how-label':         'Процесс',
        'how-h2':            'Как это работает',
        'how-desc':          'Начните и найдите свой следующий любимый ресторан за несколько минут.',
        'step1-title':       'Создать Аккаунт',
        'step1-desc':        'Зарегистрируйтесь менее чем за минуту, бесплатно.',
        'step2-title':       'Исследовать Рестораны',
        'step2-desc':        'Просматривайте сотни отобранных вариантов.',
        'step3-title':       'Спросить ИИ-Ассистента',
        'step3-desc':        'Получите гиперперсонализированные предложения.',
        'step4-title':       'Забронировать или Заказать',
        'step4-desc':        'Забронируйте столик или закажите доставку.',
        'step5-title':       'Оставить Отзыв',
        'step5-desc':        'Поделитесь своим опытом с сообществом.',
        'rest-label':        'Отборные',
        'rest-h2':           'Лучшие Рестораны',
        'rest-desc':         'Самые высокооцененные заведения Палестины',
        'rest-view-all':     'Смотреть Все',
        'card-view-btn':     'Открыть Ресторан',
        'cta-h2':            'Готовы Открывать?',
        'cta-desc':          'Присоединяйтесь к 1000+ любителям еды, открывающим лучшие рестораны Палестины каждый день.',
        'cta-btn':           'Создать Бесплатный Аккаунт',
        'footer-desc':       'Ведущая палестинская платформа для открытия и бронирования ресторанов.',
        'footer-platform':   'Платформа',
        'footer-company':    'Компания',
        'footer-about':      'О Нас',
        'footer-contact':    'Контакты',
        'footer-privacy':    'Политика Конфиденциальности',
        'footer-terms':      'Условия Использования',
        'footer-copy':       '© 2024 Yumm. Сделано с любовью к Палестине 🇵🇸',
    },
};

function applyTranslations(code) {
    const t = translations[code] || translations['en'];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (!t[key]) return;
        // Handle placeholder separately
        if (el.tagName === 'INPUT' && el.type !== 'submit') {
            el.placeholder = t[key];
        } else {
            el.textContent = t[key];
        }
    });
}

/* ─────────────────────────────
Language (navbar button)
───────────────────────────── */
let currentLang = 'ar';

function toggleLang() {
    currentLang = currentLang === 'en' ? 'ar' : 'en';
    html.lang = currentLang;
    html.dir  = currentLang === 'ar' ? 'rtl' : 'ltr';
    document.getElementById('lang-btn').textContent = currentLang === 'ar' ? 'EN' : 'العربية';
    applyTranslations(currentLang);
}

/* ─────────────────────────────
Accessibility Widget – open / close
───────────────────────────── */
function openA11y() {
    document.getElementById('a11y-widget').classList.add('open');
    document.body.style.overflow = 'hidden';
}
function closeA11y() {
    document.getElementById('a11y-widget').classList.remove('open');
    document.body.style.overflow = '';
}

/* ─────────────────────────────
Widget – Language dropdown
───────────────────────────── */
function toggleLangDrop() {
    document.getElementById('lang-drop').classList.toggle('hidden');
}
function setLang(flag, name, code, rtl) {
    document.getElementById('lang-flag').textContent = flag;
    document.getElementById('lang-name').textContent = name;
    document.getElementById('lang-drop').classList.add('hidden');
    html.lang    = code;
    html.dir     = rtl ? 'rtl' : 'ltr';
    currentLang  = code;
    document.getElementById('lang-btn').textContent = code === 'ar' ? 'EN' : 'العربية';

    applyTranslations(code);
}
document.addEventListener('click', e => {
    if (
        !e.target.closest('#lang-drop') &&
        !e.target.closest('[onclick="toggleLangDrop()"]')
    ) {
        document.getElementById('lang-drop')?.classList.add('hidden');
    }
});

/* ─────────────────────────────
Toggle a single HTML class
───────────────────────────── */
function toggleClass(cls) {
    cls.split(' ').forEach(c => html.classList.toggle(c));
    document.querySelectorAll('.a11y-opt').forEach(btn => {
        const bc = btn.getAttribute('onclick')?.match(/toggleClass\('([^']+)'\)/)?.[1];
        if (!bc) return;
        const active = bc.split(' ').some(c => html.classList.contains(c));
        btn.classList.toggle('border-[#B5451B]', active);
        btn.classList.toggle('text-[#B5451B]',   active);
    });
}

/* ─────────────────────────────
Profile toggles
───────────────────────────── */
const profiles = {};

function toggleProfile(id, classes) {
    const track = document.getElementById('tg-' + id);
    if (profiles[id]) {
        profiles[id] = false;
        track.classList.remove('on');
        classes.split(' ').forEach(c => html.classList.remove(c));
    } else {
        profiles[id] = true;
        track.classList.add('on');
        classes.split(' ').forEach(c => html.classList.add(c));
    }
}

/* ─────────────────────────────
Color mode
───────────────────────────── */
function setColorMode(m) {
    if (m === 'dark') { applyTheme(true); }
    else              { applyTheme(false); }
}

/* ─────────────────────────────
Text / Title / Background colors
───────────────────────────── */
const colorStyle = document.createElement('style');
document.head.appendChild(colorStyle);

function setTextColor(c) {
    colorStyle.textContent = c ? `body, body * { color:${c}!important; }` : '';
}
function setTitleColor(c) {
    colorStyle.textContent = c ? `h1, h2, h3, h4, h5, h6 { color:${c}!important; }` : '';
}
function setBgColor(c) { document.body.style.background = c || ''; }

/* ─────────────────────────────
Font size
───────────────────────────── */
let fs = 16;

function changeFont(d) {
    fs = Math.max(12, Math.min(28, fs + d));
    html.style.fontSize = fs + 'px';
    document.getElementById('font-val').textContent = fs === 16 ? 'Default' : fs + 'px';
    localStorage.setItem('yumm-fs', fs);
}

const sfs = localStorage.getItem('yumm-fs');
if (sfs) {
    fs = parseInt(sfs);
    html.style.fontSize = fs + 'px';
    document.getElementById('font-val').textContent = fs + 'px';
}

/* ─────────────────────────────
Line height
───────────────────────────── */
let lh = 0;

function changeLineH(d) {
    lh = Math.round((lh + d) * 10) / 10;
    lh = Math.max(-0.4, Math.min(1.2, lh));
    if (lh === 0) {
        document.body.style.lineHeight = '';
        document.getElementById('lineh-val').textContent = 'Default';
    } else {
        document.body.style.lineHeight = (1.5 + lh).toFixed(1);
        document.getElementById('lineh-val').textContent = (1.5 + lh).toFixed(1);
    }
}

/* ─────────────────────────────
Letter spacing
───────────────────────────── */
let ls = 0;

function changeLetterS(d) {
    ls = Math.round((ls + d) * 100) / 100;
    ls = Math.max(-0.1, Math.min(0.3, ls));
    if (ls === 0) {
        document.body.style.letterSpacing = '';
        document.getElementById('letters-val').textContent = 'Default';
    } else {
        document.body.style.letterSpacing = ls + 'em';
        document.getElementById('letters-val').textContent = ls + 'em';
    }
}

/* ─────────────────────────────
Content scaling
───────────────────────────── */
let scaleVal = 100;

function changeScale(d) {
    scaleVal = Math.max(70, Math.min(150, scaleVal + d));
    document.getElementById('main').style.zoom =
        scaleVal === 100 ? '' : (scaleVal / 100);
    document.getElementById('scale-val').textContent =
        scaleVal === 100 ? 'Default' : scaleVal + '%';
}

/* ─────────────────────────────
   Text alignment
───────────────────────────── */
function setTextAlign(align) {
    document.querySelectorAll('p,h1,h2,h3,li,a').forEach(el => el.style.textAlign = align);
}

/* ─────────────────────────────
   Reset all accessibility settings
───────────────────────────── */
function resetAllA11y() {
    [
        'stop-anim', 'hc-mode', 'hc-mode-light', 'monochrome',
        'low-sat', 'high-sat', 'hide-images', 'highlight-focus',
        'highlight-links', 'readable-font', 'highlight-titles'
    ].forEach(c => html.classList.remove(c));

    setTextColor(null);
    setTitleColor(null);
    setBgColor(null);

    document.body.style.lineHeight    = '';
    document.body.style.letterSpacing = '';
    document.getElementById('main').style.zoom = '';
    document.querySelectorAll('p,h1,h2,h3,li,a').forEach(el => el.style.textAlign = '');

    fs = 16; html.style.fontSize = '16px';
    lh = 0;  ls = 0;  scaleVal = 100;

    document.getElementById('font-val')  .textContent = 'Default';
    document.getElementById('lineh-val') .textContent = 'Default';
    document.getElementById('letters-val').textContent = 'Default';
    document.getElementById('scale-val') .textContent = 'Default';

    Object.keys(profiles).forEach(id => {
        profiles[id] = false;
        document.getElementById('tg-' + id)?.classList.remove('on');
    });
    document.querySelectorAll('.a11y-opt').forEach(b =>
        b.classList.remove('border-[#B5451B]', 'text-[#B5451B]')
    );

    localStorage.removeItem('yumm-fs');
}

/* ─────────────────────────────
Wishlist heart buttons
───────────────────────────── */
document.querySelectorAll('.wish-btn').forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        const icon = btn.querySelector('[data-lucide="heart"]');
        const on   = btn.getAttribute('aria-pressed') === 'true';
        icon.classList.toggle('text-[#B5451B]',  !on);
        icon.classList.toggle('fill-[#B5451B]',  !on);
        icon.classList.toggle('text-gray-400',    on);
        btn.setAttribute('aria-pressed', String(!on));
    });
});

/* ─────────────────────────────
Scroll reveal + animated counters
───────────────────────────── */
const countered = new WeakSet();

const revealObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');

        entry.target.querySelectorAll('.counter[data-target]').forEach(el => {
            if (countered.has(el)) return;
            countered.add(el);

            const target = +el.dataset.target;
            let cur = 0;
            const step = target / (1600 / 16);

            const t = setInterval(() => {
                cur = Math.min(cur + step, target);
                el.textContent = Math.floor(cur).toLocaleString();
                if (cur >= target) clearInterval(t);
            }, 16);
        });
    });
}, { threshold: 0.18 });

document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));


/* ─────────────────────────────
   Yumm — Modals JS
───────────────────────────── */

/* ── Open / Close ── */
function openModal(id) {
  document.getElementById('modal-' + id).classList.add('modal-open');
  document.body.style.overflow = 'hidden';
}
function closeModal(id) {
  document.getElementById('modal-' + id).classList.remove('modal-open');
  document.body.style.overflow = '';
}

// Close on backdrop click
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('modal-open');
    document.body.style.overflow = '';
  }
});

// Close on ESC key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-backdrop.modal-open').forEach(m => {
      m.classList.remove('modal-open');
      document.body.style.overflow = '';
    });
  }
});

/* ── Wishlist ── */
const wishlist = [
  { name: 'Al-Kanaan',             cuisine: 'Traditional Palestinian', city: 'Ramallah',  rating: '4.8' },
  { name: 'Jerusalem Garden Cafe', cuisine: 'Cafe & Breakfast',        city: 'Jerusalem', rating: '4.9' },
];

function renderWishlist() {
  const container = document.getElementById('wishlist-items');
  if (!container) return;

  if (!wishlist.length) {
    container.innerHTML = `
      <p class="text-gray-400 text-center py-8 text-sm">
        No saved restaurants yet. Hit the ♥ on any card!
      </p>`;
    return;
  }

  container.innerHTML = wishlist.map((r, i) => `
    <div class="flex items-center justify-between bg-gray-50 rounded-2xl px-4 py-3">
      <div>
        <p class="font-semibold text-sm text-gray-900">${r.name}</p>
        <p class="text-xs text-gray-400 mt-0.5">${r.cuisine} · ${r.city}</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-amber-400 font-bold text-sm">★ ${r.rating}</span>
        <button
          onclick="removeWishlist(${i})"
          class="text-xs text-red-400 hover:text-red-600 font-semibold transition-colors">
          Remove
        </button>
      </div>
    </div>
  `).join('');
}

function removeWishlist(index) {
  wishlist.splice(index, 1);
  renderWishlist();
}

/* ── AI Chat ── */
const aiMessages = [];

async function sendAIMessage() {
  const input  = document.getElementById('ai-input');
  const msg    = input.value.trim();
  if (!msg) return;

  input.value = '';
  aiMessages.push({ role: 'user', content: msg });
  renderChat();

  // Show typing indicator
  const chat = document.getElementById('ai-chat');
  const typing = document.createElement('div');
  typing.id = 'typing-indicator';
  typing.className = 'flex justify-start mb-3';
  typing.innerHTML = `
    <div class="px-4 py-2.5 rounded-2xl rounded-bl-sm bg-gray-100 text-gray-500 text-sm">
      <span class="typing-dots">●●●</span>
    </div>`;
  chat.appendChild(typing);
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 1000,
        system: `You are Yumm AI, a friendly food assistant for Palestine.
Help users discover restaurants, suggest dishes, and answer food questions about Palestinian cuisine.
Keep replies short, friendly, and practical.
Respond in the same language the user writes in (Arabic or English).
When recommending restaurants, mention ones from our platform: Al-Kanaan (Ramallah), Gaza Grill House (Gaza), Jerusalem Garden Cafe (Jerusalem).`,
        messages: aiMessages
      })
    });

    const data  = await res.json();
    const reply = data.content?.[0]?.text || 'عذراً، حدث خطأ. / Sorry, something went wrong.';
    aiMessages.push({ role: 'assistant', content: reply });
  } catch (err) {
    aiMessages.push({ role: 'assistant', content: 'عذراً، تحقق من اتصالك بالإنترنت. / Please check your connection.' });
  }

  // Remove typing indicator then render
  document.getElementById('typing-indicator')?.remove();
  renderChat();
}

function renderChat() {
  const chat = document.getElementById('ai-chat');
  if (!chat) return;

  chat.innerHTML = `
    <!-- Welcome bubble -->
    <div class="flex justify-start mb-3">
      <div class="max-w-[82%] px-4 py-2.5 rounded-2xl rounded-bl-sm bg-gray-100 text-gray-800 text-sm leading-relaxed">
        👋 مرحباً! أنا مساعد Yumm الذكي.<br>
        اسألني عن أي مطعم أو أكلة في فلسطين!<br>
        <span class="text-gray-400 text-xs">Hello! Ask me anything about Palestinian food 🍽️</span>
      </div>
    </div>
    ${aiMessages.map(m => `
      <div class="flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} mb-3">
        <div class="max-w-[82%] px-4 py-2.5 text-sm leading-relaxed
          ${m.role === 'user'
            ? 'bg-[#B5451B] text-white rounded-2xl rounded-br-sm'
            : 'bg-gray-100 text-gray-800 rounded-2xl rounded-bl-sm'}">
          ${m.content.replace(/\n/g, '<br>')}
        </div>
      </div>
    `).join('')}
  `;
  chat.scrollTop = chat.scrollHeight;
}

// Send on Enter key
document.getElementById('ai-input')?.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendAIMessage();
  }
});

/* ── Leaflet Map ── */
let yummMap = null;
let searchMarker = null;

const restaurants = [
  { lat: 31.9038, lng: 35.2034, name: 'Al-Kanaan 🍽️',             desc: 'Traditional Palestinian · Ramallah ★ 4.8' },
  { lat: 31.5017, lng: 34.4667, name: 'Gaza Grill House 🔥',        desc: 'Grills & BBQ · Gaza ★ 4.6'              },
  { lat: 31.7683, lng: 35.2137, name: 'Jerusalem Garden Cafe ☕',   desc: 'Cafe & Breakfast · Jerusalem ★ 4.9'     },
];

function initMap() {
  if (yummMap) {
    yummMap.invalidateSize();
    return;
  }

  // Load Leaflet script dynamically
  if (!window.L) {
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.onload = () => buildMap();
    document.head.appendChild(script);
  } else {
    buildMap();
  }
}

function buildMap() {
  yummMap = L.map('leaflet-map').setView([31.9, 35.2], 8);

  // OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://openstreetmap.org">OpenStreetMap</a>',
    maxZoom: 18,
  }).addTo(yummMap);

  // Custom red icon
  const redIcon = L.divIcon({
    html: `<div style="
      background:#B5451B;
      width:32px;height:32px;
      border-radius:50% 50% 50% 0;
      transform:rotate(-45deg);
      border:3px solid white;
      box-shadow:0 2px 8px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -36],
    className: '',
  });

  // Add restaurant markers
  restaurants.forEach(r => {
    L.marker([r.lat, r.lng], { icon: redIcon })
      .addTo(yummMap)
      .bindPopup(`<b>${r.name}</b><br><span style="color:#666;font-size:12px">${r.desc}</span>`, {
        maxWidth: 200
      });
  });
}

function flyToRestaurant(lat, lng, name, desc) {
  if (!yummMap) return;
  yummMap.flyTo([lat, lng], 14, { duration: 1.2 });
  setTimeout(() => {
    L.popup({ maxWidth: 200 })
      .setLatLng([lat, lng])
      .setContent(`<b>${name}</b><br><span style="color:#666;font-size:12px">${desc}</span>`)
      .openOn(yummMap);
  }, 1300);
}

async function searchMapLocation() {
  const query = document.getElementById('map-search-input')?.value.trim();
  if (!query || !yummMap) return;

  try {
    const res  = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`);
    const data = await res.json();

    if (!data.length) {
      alert('Location not found. Try a different search.');
      return;
    }

    const { lat, lon, display_name } = data[0];

    if (searchMarker) yummMap.removeLayer(searchMarker);

    searchMarker = L.marker([lat, lon])
      .addTo(yummMap)
      .bindPopup(`<b>🔍 ${query}</b><br><span style="color:#666;font-size:11px">${display_name.substring(0, 60)}...</span>`)
      .openPopup();

    yummMap.flyTo([lat, lon], 13, { duration: 1.2 });
  } catch (e) {
    alert('Search failed. Please try again.');
  }
}

// Initialize map when modal opens — patch openModal
const _origOpenModal = openModal;
window.openModal = function(id) {
  _origOpenModal(id);
  if (id === 'map') {
    setTimeout(initMap, 150); // wait for modal animation
  }
};

// Search on Enter key
document.getElementById('map-search-input')?.addEventListener('keydown', e => {
  if (e.key === 'Enter') searchMapLocation();
});


// ── contact.js — Contact Page Scripts ──

document.addEventListener('DOMContentLoaded', () => {

  const form = document.querySelector('form[action="/contact/"]');
  if (!form) return;

  // ── Client-side validation ──
  form.addEventListener('submit', (e) => {
    const name    = form.querySelector('[name="name"]');
    const email   = form.querySelector('[name="email"]');
    const message = form.querySelector('[name="message"]');

    clearErrors();

    let valid = true;

    if (!name.value.trim()) {
      showError(name, 'Name is required.');
      valid = false;
    }

    if (!email.value.trim() || !email.value.includes('@')) {
      showError(email, 'Please enter a valid email address.');
      valid = false;
    }

    if (!message.value.trim() || message.value.trim().length < 10) {
      showError(message, 'Message must be at least 10 characters.');
      valid = false;
    }

    if (!valid) e.preventDefault();
  });

  function showError(field, msg) {
    field.classList.add('border-red-500');
    const err = document.createElement('p');
    err.className = 'text-red-400 text-xs mt-1 field-error';
    err.textContent = msg;
    field.parentElement.appendChild(err);
  }

  function clearErrors() {
    document.querySelectorAll('.field-error').forEach(e => e.remove());
    form.querySelectorAll('input, textarea').forEach(f => f.classList.remove('border-red-500'));
  }

  // ── Character counter for message ──
  const textarea = form.querySelector('[name="message"]');
  if (textarea) {
    const counter = document.createElement('p');
    counter.className = 'text-xs text-gray-500 mt-1 text-right';
    counter.textContent = '0 / 1000';
    textarea.parentElement.appendChild(counter);

    textarea.addEventListener('input', () => {
      const len = textarea.value.length;
      counter.textContent = `${len} / 1000`;
      counter.classList.toggle('text-orange', len > 900);
    });
  }

});


// ── legal.js — Privacy & Terms Pages ──

document.addEventListener('DOMContentLoaded', () => {

  // Smooth scroll for TOC links (enhances native scroll-behavior)
  document.querySelectorAll('aside nav a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.pushState(null, '', link.getAttribute('href'));
      }
    });
  });

  // "Back to top" button — appears after scrolling past 400px
  const topBtn = document.createElement('button');
  topBtn.textContent = '↑';
  topBtn.title = 'Back to top';
  topBtn.className = [
    'fixed', 'bottom-24', 'right-6',
    'w-10', 'h-10', 'rounded-full',
    'bg-dark-700', 'border', 'border-dark-600',
    'text-gray-400', 'hover:bg-orange', 'hover:text-white',
    'transition-all', 'duration-200',
    'opacity-0', 'pointer-events-none',
    'text-sm', 'font-bold', 'z-40'
  ].join(' ');
  document.body.appendChild(topBtn);

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      topBtn.classList.remove('opacity-0', 'pointer-events-none');
    } else {
      topBtn.classList.add('opacity-0', 'pointer-events-none');
    }
  });

  topBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

});



function toggleSidebar() {
  const sidebar = document.getElementById('mobileSidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (!sidebar || !overlay) return;
  const isOpen = !sidebar.classList.contains('translate-x-full');
  sidebar.classList.toggle('translate-x-full', isOpen);
  overlay.classList.toggle('hidden', isOpen);
}

function toggleUserMenu() {
  const menu = document.getElementById('userMenu');
  if (menu) menu.classList.toggle('hidden');
}

document.addEventListener('click', function(e) {
  const menu = document.getElementById('userMenu');
  if (!menu) return;
  if (!e.target.closest('#userMenu') && !e.target.closest('[onclick="toggleUserMenu()"]')) {
    menu.classList.add('hidden');
  }
});