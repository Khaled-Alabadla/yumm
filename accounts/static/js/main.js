/* ─────────────────────────────
   Yumm — Main JavaScript
───────────────────────────── */

lucide.createIcons();

/* ─────────────────────────────
   Theme (dark / light)
───────────────────────────── */
const html = document.documentElement;

function applyTheme(dark) {
  html.classList.toggle('dark', dark);
  document.getElementById('icon-moon')?.classList.toggle('hidden',  dark);
  document.getElementById('icon-sun') ?.classList.toggle('hidden', !dark);
  document.getElementById('theme-btn')?.setAttribute('aria-pressed', String(dark));
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
  d.textContent = now.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' });
}
updateClock();
setInterval(updateClock, 1000);

/* ─────────────────────────────
   Translations
───────────────────────────── */
const translations = {
  en: {
    'nav-home': 'Home', 'nav-restaurants': 'Restaurants', 'nav-ai': 'AI Assistant',
    'nav-login': 'Login', 'nav-register': 'Register',
    'hero-badge': "Palestine's #1 Food Platform",
    'hero-h1-line1': 'Discover the Best', 'hero-h1-span': 'Restaurants', 'hero-h1-line2': 'in Palestine',
    'hero-desc': 'Explore menus, reviews, ratings, reservations, and AI-powered recommendations — all in one place.',
    'hero-search-ph': 'Search restaurants, cuisines, cities...', 'hero-search-btn': 'Search',
    'hero-cta1': 'Explore Restaurants', 'hero-cta2': 'Ask AI Assistant',
    'stat-restaurants': 'Restaurants', 'stat-reviews': 'Reviews', 'stat-users': 'Happy Users', 'stat-rated': 'Top Rated',
    'feat-label': 'Features', 'feat-h2': 'Everything You Need',
    'feat-desc': 'A complete platform for discovering, reviewing, and reserving the best dining in Palestine.',
    'feat1-title': 'AI Assistant', 'feat1-desc': 'Describe your craving and our AI finds the perfect match instantly.', 'feat1-link': 'Try it',
    'feat2-title': 'Interactive Map', 'feat2-desc': 'Discover restaurants near you on a live, interactive map.', 'feat2-link': 'Open Map',
    'feat3-title': 'Reviews & Ratings', 'feat3-desc': 'Honest reviews from a trusted Palestinian food community.', 'feat3-link': 'Read Reviews',
    'feat4-title': 'Wishlist', 'feat4-desc': 'Save your favourite restaurants for future visits.', 'feat4-link': 'View Saved',
    'how-label': 'Process', 'how-h2': 'How It Works', 'how-desc': 'Get started and find your next favourite restaurant in minutes.',
    'step1-title': 'Create Account', 'step1-desc': 'Register in under a minute, for free.',
    'step2-title': 'Explore Restaurants', 'step2-desc': 'Browse hundreds of curated options.',
    'step3-title': 'Ask AI Assistant', 'step3-desc': 'Get hyper-personalised suggestions.',
    'step4-title': 'Leave a Review', 'step4-desc': 'Share your experience with the community.',
    'rest-label': 'Handpicked', 'rest-h2': 'Top Restaurants', 'rest-desc': 'Highest-rated picks across Palestine',
    'rest-view-all': 'View All', 'card-view-btn': 'View Restaurant',
    'badge-open': 'Open',
    'cuisine-traditional': 'Traditional Palestinian', 'cuisine-grill': 'Grills & BBQ', 'cuisine-cafe': 'Cafe & Breakfast',
    'tag-family': 'Family',
    'cta-h2': 'Ready to Explore?', 'cta-desc': "Join 1000+ food lovers discovering Palestine's best restaurants every day.", 'cta-btn': 'Create Account',
    'footer-desc': "Palestine's leading restaurant discovery and reservation platform.",
    'footer-platform': 'Platform', 'footer-company': 'Company', 'footer-about': 'About Us',
    'footer-contact': 'Contact', 'footer-privacy': 'Privacy Policy', 'footer-terms': 'Terms of Service',
    'footer-copy': '© 2024 Yumm. Made with love for Palestine 🇵🇸',
    // A11y widget
    'a11y-title': 'Accessibility Adjustments', 'a11y-reset': 'Reset Settings',
    'a11y-content': 'Content Adjustments', 'a11y-scale': 'Content Scaling',
    'a11y-readable': 'Readable Font', 'a11y-htitles': 'Highlight Titles',
    'a11y-hlinks': 'Highlight Links', 'a11y-center': 'Align Center',
    'a11y-left': 'Align Left', 'a11y-right': 'Align Right',
    'a11y-font': 'Adjust Font Sizing', 'a11y-lineh': 'Adjust Line Height',
    'a11y-letters': 'Adjust Letter Spacing',
    'a11y-colors': 'Color Adjustments', 'a11y-dark': 'Dark Contrast',
    'a11y-light': 'Light Contrast', 'a11y-hc': 'High Contrast',
    'a11y-highsat': 'High Saturation', 'a11y-mono': 'Monochrome', 'a11y-lowsat': 'Low Saturation',
    'a11y-textcol': 'Adjust Text Colors', 'a11y-titlecol': 'Adjust Title Colors',
    'a11y-bgcol': 'Adjust Background Colors', 'a11y-cancel': 'Cancel',
    'a11y-orient': 'Orientation Adjustments', 'a11y-hideimg': 'Hide Images',
    'a11y-stopanim': 'Stop Animations', 'a11y-hlfocus': 'Highlight Focus',
    'a11y-mute': 'Mute Sounds', 'a11y-links': 'Useful Links',
    'a11y-footer': 'Web Accessibility by Yumm ♿',
    'a11y-default': 'Default',
  },
  ar: {
    'nav-home': 'الرئيسية', 'nav-restaurants': 'المطاعم', 'nav-ai': 'مساعد الذكاء الاصطناعي',
    'nav-login': 'تسجيل الدخول', 'nav-register': 'إنشاء حساب',
    'hero-badge': 'منصة الطعام الأولى في فلسطين',
    'hero-h1-line1': 'اكتشف أفضل', 'hero-h1-span': 'المطاعم', 'hero-h1-line2': 'في فلسطين',
    'hero-desc': 'استكشف القوائم والتقييمات والحجوزات وتوصيات الذكاء الاصطناعي — كل شيء في مكان واحد.',
    'hero-search-ph': 'ابحث عن مطاعم، مأكولات، مدن...', 'hero-search-btn': 'بحث',
    'hero-cta1': 'استكشف المطاعم', 'hero-cta2': 'اسأل المساعد الذكي',
    'stat-restaurants': 'مطعم', 'stat-reviews': 'تقييم', 'stat-users': 'مستخدم سعيد', 'stat-rated': 'الأعلى تقييماً',
    'feat-label': 'المميزات', 'feat-h2': 'كل ما تحتاجه',
    'feat-desc': 'منصة متكاملة لاكتشاف أفضل المطاعم الفلسطينية ومراجعتها وحجزها.',
    'feat1-title': 'المساعد الذكي', 'feat1-desc': 'صف ما تشتهيه وسيجد ذكاؤنا الاصطناعي التطابق المثالي على الفور.', 'feat1-link': 'جرّبه',
    'feat2-title': 'خريطة تفاعلية', 'feat2-desc': 'اكتشف المطاعم القريبة منك على خريطة حية وتفاعلية.', 'feat2-link': 'افتح الخريطة',
    'feat3-title': 'مراجعات وتقييمات', 'feat3-desc': 'مراجعات صادقة من مجتمع طعام فلسطيني موثوق.', 'feat3-link': 'اقرأ التقييمات',
    'feat4-title': 'قائمة المفضلة', 'feat4-desc': 'احفظ مطاعمك المفضلة لزيارات مستقبلية.', 'feat4-link': 'عرض المحفوظات',
    'how-label': 'كيف يعمل', 'how-h2': 'كيف يعمل التطبيق', 'how-desc': 'ابدأ واعثر على مطعمك المفضل القادم في دقائق.',
    'step1-title': 'إنشاء حساب', 'step1-desc': 'سجّل في أقل من دقيقة، مجاناً.',
    'step2-title': 'استكشف المطاعم', 'step2-desc': 'تصفح مئات الخيارات المنتقاة.',
    'step3-title': 'اسأل المساعد الذكي', 'step3-desc': 'احصل على اقتراحات مخصصة لك.',
    'step4-title': 'اترك تقييماً', 'step4-desc': 'شارك تجربتك مع المجتمع.',
    'rest-label': 'مختارة بعناية', 'rest-h2': 'أفضل المطاعم', 'rest-desc': 'أعلى التقييمات في جميع أنحاء فلسطين',
    'rest-view-all': 'عرض الكل', 'card-view-btn': 'عرض المطعم',
    'badge-open': 'مفتوح',
    'cuisine-traditional': 'فلسطيني أصيل', 'cuisine-grill': 'مشاوي وشواء', 'cuisine-cafe': 'كافيه وفطور',
    'tag-family': 'عائلي',
    'cta-h2': 'مستعد للاستكشاف؟', 'cta-desc': 'انضم إلى أكثر من 1000 محب للطعام يكتشفون أفضل مطاعم فلسطين كل يوم.', 'cta-btn': 'إنشاء حساب',
    'footer-desc': 'منصة فلسطين الرائدة لاكتشاف المطاعم وحجزها.',
    'footer-platform': 'المنصة', 'footer-company': 'الشركة', 'footer-about': 'من نحن',
    'footer-contact': 'تواصل معنا', 'footer-privacy': 'سياسة الخصوصية', 'footer-terms': 'شروط الخدمة',
    'footer-copy': '© 2024 Yumm. صُنع بحب لفلسطين 🇵🇸',
    // A11y widget - Arabic ✅ كاملة
    'a11y-title': 'إعدادات إمكانية الوصول', 'a11y-reset': 'إعادة الضبط',
    'a11y-content': 'ضبط المحتوى', 'a11y-scale': 'تغيير حجم المحتوى',
    'a11y-readable': 'خط سهل القراءة', 'a11y-htitles': 'إبراز العناوين',
    'a11y-hlinks': 'إبراز الروابط', 'a11y-center': 'توسيط النص',
    'a11y-left': 'محاذاة يسار', 'a11y-right': 'محاذاة يمين',
    'a11y-font': 'ضبط حجم الخط', 'a11y-lineh': 'ضبط ارتفاع السطر',
    'a11y-letters': 'ضبط تباعد الأحرف',
    'a11y-colors': 'ضبط الألوان', 'a11y-dark': 'تباين داكن',
    'a11y-light': 'تباين فاتح', 'a11y-hc': 'تباين عالٍ',
    'a11y-highsat': 'إشباع ألوان عالٍ', 'a11y-mono': 'أحادي اللون', 'a11y-lowsat': 'إشباع ألوان منخفض',
    'a11y-textcol': 'ضبط لون النص', 'a11y-titlecol': 'ضبط لون العناوين',
    'a11y-bgcol': 'ضبط لون الخلفية', 'a11y-cancel': 'إلغاء',
    'a11y-orient': 'ضبط الاتجاه', 'a11y-hideimg': 'إخفاء الصور',
    'a11y-stopanim': 'إيقاف الحركات', 'a11y-hlfocus': 'إبراز التركيز',
    'a11y-mute': 'كتم الأصوات', 'a11y-links': 'روابط مفيدة',
    'a11y-footer': 'إمكانية الوصول بواسطة Yumm ♿',
    'a11y-default': 'الافتراضي',
  },
};

/* ─────────────────────────────
   Apply translations to page
───────────────────────────── */
function applyTranslations(code) {
  const t = translations[code] || translations['en'];

  // data-i18n على النصوص العادية
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (!t[key]) return;
    el.textContent = t[key];
  });

  // data-i18n-placeholder على الـ inputs
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (t[key]) el.placeholder = t[key];
  });
}

/* ─────────────────────────────
   Language toggle 
───────────────────────────── */
//
let currentLang = localStorage.getItem('yumm-lang') || 'en';

function applyLang(code) {
  currentLang = code;
  const isRtl = (code === 'ar');
  html.lang = code;
  html.dir  = isRtl ? 'rtl' : 'ltr';

  const langBtn = document.getElementById('lang-btn');
  if (langBtn) langBtn.textContent = isRtl ? 'EN' : 'العربية';

  const flagEl = document.getElementById('lang-flag');
  const nameEl = document.getElementById('lang-name');
  if (flagEl) flagEl.textContent = isRtl ? '🇸🇦' : '🇺🇸';
  if (nameEl) nameEl.textContent = isRtl ? 'ARABIC' : 'ENGLISH (US)';

  localStorage.setItem('yumm-lang', code);
  applyTranslations(code);
}

function toggleLang() {

  applyLang(currentLang === 'en' ? 'ar' : 'en');
}


applyLang(currentLang);

/* ─────────────────────────────
   Accessibility Widget — open / close
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
   Widget — Language dropdown (inside a11y panel)
───────────────────────────── */
function toggleLangDrop() {
  document.getElementById('lang-drop').classList.toggle('hidden');
}

function setLang(flag, name, code, rtl) {
  document.getElementById('lang-flag').textContent = flag;
  document.getElementById('lang-name').textContent = name;
  document.getElementById('lang-drop').classList.add('hidden');
  applyLang(code);
}

document.addEventListener('click', e => {
  if (!e.target.closest('#lang-drop') && !e.target.closest('[onclick="toggleLangDrop()"]')) {
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
   Color mode
───────────────────────────── */
function setColorMode(m) {
  applyTheme(m === 'dark');
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
  colorStyle.textContent = c ? `h1,h2,h3,h4,h5,h6 { color:${c}!important; }` : '';
}
function setBgColor(c) { document.body.style.background = c || ''; }

/* ─────────────────────────────
   Font size
───────────────────────────── */
let fs = 16;

function changeFont(d) {
  fs = Math.max(12, Math.min(28, fs + d));
  html.style.fontSize = fs + 'px';
  const def = translations[currentLang]?.['a11y-default'] || 'Default';
  document.getElementById('font-val').textContent = fs === 16 ? def : fs + 'px';
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
  const def = translations[currentLang]?.['a11y-default'] || 'Default';
  if (lh === 0) {
    document.body.style.lineHeight = '';
    document.getElementById('lineh-val').textContent = def;
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
  const def = translations[currentLang]?.['a11y-default'] || 'Default';
  if (ls === 0) {
    document.body.style.letterSpacing = '';
    document.getElementById('letters-val').textContent = def;
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
  const def = translations[currentLang]?.['a11y-default'] || 'Default';
  document.getElementById('main').style.zoom = scaleVal === 100 ? '' : (scaleVal / 100);
  document.getElementById('scale-val').textContent = scaleVal === 100 ? def : scaleVal + '%';
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
  ['stop-anim','hc-mode','hc-mode-light','monochrome','low-sat','high-sat',
   'hide-images','highlight-focus','highlight-links','readable-font','highlight-titles'
  ].forEach(c => html.classList.remove(c));

  setTextColor(null);
  setTitleColor(null);
  setBgColor(null);

  document.body.style.lineHeight    = '';
  document.body.style.letterSpacing = '';
  document.getElementById('main').style.zoom = '';
  document.querySelectorAll('p,h1,h2,h3,li,a').forEach(el => el.style.textAlign = '');

  const def = translations[currentLang]?.['a11y-default'] || 'Default';
  fs = 16; html.style.fontSize = '16px';
  lh = 0;  ls = 0;  scaleVal = 100;

  document.getElementById('font-val')  .textContent = def;
  document.getElementById('lineh-val') .textContent = def;
  document.getElementById('letters-val').textContent = def;
  document.getElementById('scale-val') .textContent = def;

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
    icon.classList.toggle('text-[#B5451B]', !on);
    icon.classList.toggle('fill-[#B5451B]', !on);
    icon.classList.toggle('text-gray-400',   on);
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

<<<<<<< Updated upstream
/* ─────────────────────────────
   Modals — open / close
───────────────────────────── */
function openModal(id) {
  document.getElementById('modal-' + id).classList.add('modal-open');
  document.body.style.overflow = 'hidden';
  if (id === 'map') setTimeout(initMap, 150);
=======

/* ─────────────────────────────
   Yumm — Modals JS
───────────────────────────── */

/* ── Open / Close ── */
function openModal(id) {
  document.getElementById('modal-' + id).classList.add('modal-open');
  document.body.style.overflow = 'hidden';
>>>>>>> Stashed changes
}
function closeModal(id) {
  document.getElementById('modal-' + id).classList.remove('modal-open');
  document.body.style.overflow = '';
}

<<<<<<< Updated upstream
=======
// Close on backdrop click
>>>>>>> Stashed changes
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('modal-open');
    document.body.style.overflow = '';
  }
});

<<<<<<< Updated upstream
=======
// Close on ESC key
>>>>>>> Stashed changes
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-backdrop.modal-open').forEach(m => {
      m.classList.remove('modal-open');
      document.body.style.overflow = '';
    });
  }
});

<<<<<<< Updated upstream
/* ─────────────────────────────
   Wishlist data + render
───────────────────────────── */
=======
/* ── Wishlist ── */
>>>>>>> Stashed changes
const wishlist = [
  { name: 'Al-Kanaan',             cuisine: 'Traditional Palestinian', city: 'Ramallah',  rating: '4.8' },
  { name: 'Jerusalem Garden Cafe', cuisine: 'Cafe & Breakfast',        city: 'Jerusalem', rating: '4.9' },
];

function renderWishlist() {
  const container = document.getElementById('wishlist-items');
  if (!container) return;
<<<<<<< Updated upstream
  if (!wishlist.length) {
    container.innerHTML = `<p class="text-gray-400 text-center py-8 text-sm">No saved restaurants yet. Hit the ♥ on any card!</p>`;
    return;
  }
=======

  if (!wishlist.length) {
    container.innerHTML = `
      <p class="text-gray-400 text-center py-8 text-sm">
        No saved restaurants yet. Hit the ♥ on any card!
      </p>`;
    return;
  }

>>>>>>> Stashed changes
  container.innerHTML = wishlist.map((r, i) => `
    <div class="flex items-center justify-between bg-gray-50 rounded-2xl px-4 py-3">
      <div>
        <p class="font-semibold text-sm text-gray-900">${r.name}</p>
        <p class="text-xs text-gray-400 mt-0.5">${r.cuisine} · ${r.city}</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-amber-400 font-bold text-sm">★ ${r.rating}</span>
<<<<<<< Updated upstream
        <button onclick="removeWishlist(${i})" class="text-xs text-red-400 hover:text-red-600 font-semibold transition-colors">Remove</button>
=======
        <button
          onclick="removeWishlist(${i})"
          class="text-xs text-red-400 hover:text-red-600 font-semibold transition-colors">
          Remove
        </button>
>>>>>>> Stashed changes
      </div>
    </div>
  `).join('');
}

function removeWishlist(index) {
  wishlist.splice(index, 1);
  renderWishlist();
}

<<<<<<< Updated upstream
/* ─────────────────────────────
   AI Chat
───────────────────────────── */
const aiMessages = [];

async function sendAIMessage() {
  const input = document.getElementById('ai-input');
  const msg   = input.value.trim();
  if (!msg) return;
=======
/* ── AI Chat ── */
const aiMessages = [];

async function sendAIMessage() {
  const input  = document.getElementById('ai-input');
  const msg    = input.value.trim();
  if (!msg) return;

>>>>>>> Stashed changes
  input.value = '';
  aiMessages.push({ role: 'user', content: msg });
  renderChat();

<<<<<<< Updated upstream
=======
  // Show typing indicator
>>>>>>> Stashed changes
  const chat = document.getElementById('ai-chat');
  const typing = document.createElement('div');
  typing.id = 'typing-indicator';
  typing.className = 'flex justify-start mb-3';
<<<<<<< Updated upstream
  typing.innerHTML = `<div class="px-4 py-2.5 rounded-2xl rounded-bl-sm bg-gray-100 text-gray-500 text-sm"><span class="typing-dots">●●●</span></div>`;
=======
  typing.innerHTML = `
    <div class="px-4 py-2.5 rounded-2xl rounded-bl-sm bg-gray-100 text-gray-500 text-sm">
      <span class="typing-dots">●●●</span>
    </div>`;
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        messages: aiMessages,
      }),
    });
    const data  = await res.json();
    const reply = data.content?.[0]?.text || 'عذراً، حدث خطأ. / Sorry, something went wrong.';
    aiMessages.push({ role: 'assistant', content: reply });
  } catch {
    aiMessages.push({ role: 'assistant', content: 'عذراً، تحقق من اتصالك. / Please check your connection.' });
  }

=======
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
>>>>>>> Stashed changes
  document.getElementById('typing-indicator')?.remove();
  renderChat();
}

function renderChat() {
  const chat = document.getElementById('ai-chat');
  if (!chat) return;
<<<<<<< Updated upstream
  chat.innerHTML = `
=======

  chat.innerHTML = `
    <!-- Welcome bubble -->
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
document.getElementById('ai-input')?.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendAIMessage(); }
});

/* ─────────────────────────────
   Leaflet Map
───────────────────────────── */
=======
// Send on Enter key
document.getElementById('ai-input')?.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendAIMessage();
  }
});

/* ── Leaflet Map ── */
>>>>>>> Stashed changes
let yummMap = null;
let searchMarker = null;

const restaurants = [
<<<<<<< Updated upstream
  { lat: 31.9038, lng: 35.2034, name: 'Al-Kanaan 🍽️',           desc: 'Traditional Palestinian · Ramallah ★ 4.8' },
  { lat: 31.5017, lng: 34.4667, name: 'Gaza Grill House 🔥',      desc: 'Grills & BBQ · Gaza ★ 4.6'              },
  { lat: 31.7683, lng: 35.2137, name: 'Jerusalem Garden Cafe ☕', desc: 'Cafe & Breakfast · Jerusalem ★ 4.9'     },
];

function initMap() {
  if (yummMap) { yummMap.invalidateSize(); return; }
=======
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
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://openstreetmap.org">OpenStreetMap</a>', maxZoom: 18,
  }).addTo(yummMap);

  const redIcon = L.divIcon({
    html: `<div style="background:#B5451B;width:32px;height:32px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>`,
    iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -36], className: '',
  });

  restaurants.forEach(r => {
    L.marker([r.lat, r.lng], { icon: redIcon })
      .addTo(yummMap)
      .bindPopup(`<b>${r.name}</b><br><span style="color:#666;font-size:12px">${r.desc}</span>`, { maxWidth: 200 });
=======

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
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
  try {
    const res  = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`);
    const data = await res.json();
    if (!data.length) { alert('Location not found. Try a different search.'); return; }
    const { lat, lon, display_name } = data[0];
    if (searchMarker) yummMap.removeLayer(searchMarker);
    searchMarker = L.marker([lat, lon]).addTo(yummMap)
      .bindPopup(`<b>🔍 ${query}</b><br><span style="color:#666;font-size:11px">${display_name.substring(0, 60)}...</span>`)
      .openPopup();
    yummMap.flyTo([lat, lon], 13, { duration: 1.2 });
  } catch { alert('Search failed. Please try again.'); }
}

=======

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
>>>>>>> Stashed changes
document.getElementById('map-search-input')?.addEventListener('keydown', e => {
  if (e.key === 'Enter') searchMapLocation();
});

<<<<<<< Updated upstream
/* ─────────────────────────────
   Sidebar & User Menu
───────────────────────────── */
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

/* ─────────────────────────────
   Contact form validation
───────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form[action="/contact/"]');
  if (!form) return;
  form.addEventListener('submit', e => {
    const name    = form.querySelector('[name="name"]');
    const email   = form.querySelector('[name="email"]');
    const message = form.querySelector('[name="message"]');
    clearErrors();
    let valid = true;
    if (!name.value.trim()) { showError(name, 'Name is required.'); valid = false; }
    if (!email.value.trim() || !email.value.includes('@')) { showError(email, 'Please enter a valid email.'); valid = false; }
    if (!message.value.trim() || message.value.trim().length < 10) { showError(message, 'Message must be at least 10 characters.'); valid = false; }
    if (!valid) e.preventDefault();
  });
=======

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

>>>>>>> Stashed changes
  function showError(field, msg) {
    field.classList.add('border-red-500');
    const err = document.createElement('p');
    err.className = 'text-red-400 text-xs mt-1 field-error';
    err.textContent = msg;
    field.parentElement.appendChild(err);
  }
<<<<<<< Updated upstream
  function clearErrors() {
    document.querySelectorAll('.field-error').forEach(e => e.remove());
    form.querySelectorAll('input,textarea').forEach(f => f.classList.remove('border-red-500'));
  }
=======

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

>>>>>>> Stashed changes
});



<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
