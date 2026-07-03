/* ─────────────────────────────
   Yumm — Main JavaScript
───────────────────────────── */

document.documentElement.classList.add("js");

if (window.lucide) {
  lucide.createIcons();
}

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
function getClockLocale() {
  const lang = document.documentElement.lang || 'en';
  return lang.startsWith('ar') ? 'ar-PS' : 'en-US';
}

function updateClock() {
  const now = new Date();
  const t = document.getElementById('clock-time');
  const d = document.getElementById('clock-date');
  if (!t || !d) return;
  const locale = getClockLocale();
  t.textContent = now.toLocaleTimeString(locale, {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
  d.textContent = now.toLocaleDateString(locale, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  });
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
        'hero-desc':         'Explore menus, reviews, ratings, and our AI Assistant — all in one place.',
        'hero-search-ph':    'Search restaurants...',
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
        'footer-desc':       "Palestine's leading restaurant discovery and review platform. Find exceptional dining across every city.",
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
        'hero-desc':         'استكشف القوائم والتقييمات ومساعد الذكاء الاصطناعي — كل شيء في مكان واحد.',
        'hero-search-ph':    'ابحث عن مطاعم...',
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
        'footer-desc':       'منصة فلسطين الرائدة لاكتشاف المطاعم وتقييمها. اعثر على أرقى تجارب الطعام في كل مدينة.',
        'footer-platform':   'المنصة',
        'footer-company':    'الشركة',
        'footer-about':      'من نحن',
        'footer-contact':    'تواصل معنا',
        'footer-privacy':    'سياسة الخصوصية',
        'footer-terms':      'شروط الخدمة',
        'footer-copy':       '© 2024 Yumm. صُنع بحب لفلسطين 🇵🇸',
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

function submitSiteLanguage(code) {
    const form = document.getElementById('lang-form');
    if (!form) return false;
    const input = form.querySelector('input[name="language"]');
    if (input) input.value = code;
    form.submit();
    return true;
}

/* ─────────────────────────────
   Language toggle 
───────────────────────────── */
let currentLang = document.documentElement.lang?.startsWith('ar') ? 'ar' : 'en';

function toggleLang() {
    submitSiteLanguage(currentLang === 'ar' ? 'en' : 'ar');
}


applyTranslations(currentLang);

/* ─────────────────────────────
   Accessibility Widget — open / close
───────────────────────────── */
function openA11y() {
    const widget = document.getElementById('a11y-widget');
    if (!widget) return;
    widget.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (window.lucide) lucide.createIcons();
}

function closeA11y() {
    const widget = document.getElementById('a11y-widget');
    if (!widget) return;
    widget.classList.remove('open');
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

    if (code === 'ar' || code === 'en') {
        submitSiteLanguage(code);
        return;
    }

    html.lang    = code;
    html.dir     = rtl ? 'rtl' : 'ltr';
    currentLang  = code;
    const btn = document.getElementById('lang-btn');
    if (btn) btn.textContent = code === 'ar' ? 'EN' : 'ع';

    applyTranslations(code);
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

function defaultFontLabel() {
    return document.getElementById('font-val')?.dataset.defaultLabel || 'Default';
}

function changeFont(d) {
    fs = Math.max(12, Math.min(28, fs + d));
    html.style.fontSize = fs + 'px';
    const fontVal = document.getElementById('font-val');
    if (fontVal) {
        fontVal.textContent = fs === 16 ? defaultFontLabel() : fs + 'px';
    }
    localStorage.setItem('yumm-fs', fs);
}

const sfs = localStorage.getItem('yumm-fs');
if (sfs) {
    fs = parseInt(sfs);
    html.style.fontSize = fs + 'px';
    const fontVal = document.getElementById('font-val');
    if (fontVal) fontVal.textContent = fs + 'px';
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
    document.getElementById('main')?.style && (document.getElementById('main').style.zoom = '');
    document.querySelectorAll('p,h1,h2,h3,li,a').forEach(el => el.style.textAlign = '');

  const def = translations[currentLang]?.['a11y-default'] || 'Default';
  fs = 16; html.style.fontSize = '16px';
  lh = 0;  ls = 0;  scaleVal = 100;

    const fontVal = document.getElementById('font-val');
    if (fontVal) fontVal.textContent = defaultFontLabel();
    const linehVal = document.getElementById('lineh-val');
    if (linehVal) linehVal.textContent = 'Default';
    const lettersVal = document.getElementById('letters-val');
    if (lettersVal) lettersVal.textContent = 'Default';
    const scaleValEl = document.getElementById('scale-val');
    if (scaleValEl) scaleValEl.textContent = 'Default';

  document.querySelectorAll('.a11y-opt').forEach(b =>
    b.classList.remove('border-[#B5451B]', 'text-[#B5451B]')
  );

  localStorage.removeItem('yumm-fs');
}

/* ─────────────────────────────
   Toast notifications
───────────────────────────── */
function getWishlistI18n() {
  const el = document.getElementById('wishlist-i18n');
  if (!el) return {};
  try {
    return JSON.parse(el.textContent);
  } catch {
    return {};
  }
}

function showYummToast(message, type = 'success') {
  const root = document.getElementById('yumm-toast-root');
  if (!root || !message) return;
  const text = String(message).replace(/[\u{1F300}-\u{1FAFF}\u2600-\u27BF]/gu, '').trim();
  const toast = document.createElement('div');
  toast.className = `yumm-toast yumm-toast--${type}`;
  toast.innerHTML = `<span class="yumm-toast__text">${text}</span>`;
  root.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('is-visible'));
  setTimeout(() => {
    toast.classList.remove('is-visible');
    setTimeout(() => toast.remove(), 280);
  }, 2800);
}
window.showYummToast = showYummToast;

/* ─────────────────────────────
   Wishlist AJAX (landing + public cards + detail)
───────────────────────────── */
function updateWishlistFabBadge() {
  const badge = document.querySelector('.yumm-fab-wishlist__badge');
  const fab = document.querySelector('.yumm-fab-wishlist');
  if (!fab) return;
  const count = getWishlist().length;
  if (badge) {
    badge.textContent = String(count);
    badge.hidden = count === 0;
  } else if (count > 0) {
    const el = document.createElement('span');
    el.className = 'yumm-fab-wishlist__badge';
    el.textContent = String(count);
    fab.appendChild(el);
  }
}

function updateWishlistCacheFromForm(form, added) {
  const source = form.closest('[data-restaurant-id]') || form;
  const id = parseInt(source.dataset.restaurantId, 10);
  if (!id) return;
  let list = [...getWishlist()];
  if (added) {
    if (!list.some((item) => item.id === id)) {
      list.unshift({
        id,
        name: source.dataset.restaurantName || '',
        cuisine: source.dataset.restaurantCuisine || '',
        city: source.dataset.restaurantCity || '',
        rating: source.dataset.restaurantRating || '',
        url: source.dataset.restaurantUrl || '',
      });
    }
  } else {
    list = list.filter((item) => item.id !== id);
  }
  wishlistCache = list;
  updateWishlistFabBadge();
}

function syncWishlistButtonState(btn, added) {
  if (!btn) return;
  btn.classList.toggle('is-active', added);
  btn.setAttribute('aria-pressed', added ? 'true' : 'false');
  const icon = btn.querySelector('[data-lucide="heart"]');
  if (icon) {
    icon.classList.toggle('text-[#B5451B]', added);
    icon.classList.toggle('fill-[#B5451B]', added);
    icon.classList.toggle('text-gray-400', !added);
  }
  const label = btn.querySelector('.rp-wishlist-btn__label');
  const form = btn.closest('form');
  if (label && form) {
    label.textContent = added
      ? (form.dataset.labelRemove || 'Remove from Wishlist')
      : (form.dataset.labelAdd || 'Add to Wishlist');
  }
}

function initWishlistAjax() {
  document.querySelectorAll('.landing-wishlist-form[data-ajax="1"], .rp-wishlist-form[data-ajax="1"]').forEach((form) => {
    if (form.dataset.wishlistBound) return;
    form.dataset.wishlistBound = '1';
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      const btn = form.querySelector('.wish-btn, .rp-wishlist-btn, .rp-action-btn');
      const csrf = form.querySelector('[name=csrfmiddlewaretoken]');
      const i = getWishlistI18n();
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf ? csrf.value : '',
          },
          body: new FormData(form),
        });
        const data = await res.json();
        if (!data.success) {
          showYummToast(data.message || i.loginRequired || 'Action failed', 'info');
          return;
        }
        syncWishlistButtonState(btn, data.added);
        updateWishlistCacheFromForm(form, data.added);
        if (document.getElementById('modal-wishlist')?.classList.contains('modal-open')) {
          renderWishlist();
        }
        showYummToast(
          data.message || (data.added ? i.added : i.removed) || 'Saved',
          data.added ? 'success' : 'removed',
        );
      } catch {
        form.submit();
      }
    });
  });
}
window.initWishlistAjax = initWishlistAjax;

document.querySelectorAll('.wish-btn-guest, .rp-wishlist-btn--guest').forEach((link) => {
  link.addEventListener('click', () => {
    const i = getWishlistI18n();
    showYummToast(i.loginRequired || 'Please log in to save restaurants', 'info');
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
   Modals — open / close
───────────────────────────── */
function openModal(id) {
  document.getElementById('modal-' + id).classList.add('modal-open');
  document.body.style.overflow = 'hidden';
  if (id === 'map') setTimeout(initMap, 150);
  if (id === 'wishlist') {
    renderWishlist();
    if (window.lucide) lucide.createIcons();
  }
}
function closeModal(id) {
  document.getElementById('modal-' + id).classList.remove('modal-open');
  document.body.style.overflow = '';
}

document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('modal-open');
    document.body.style.overflow = '';
  }
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-backdrop.modal-open').forEach(m => {
      m.classList.remove('modal-open');
      document.body.style.overflow = '';
    });
  }
});

/* ─────────────────────────────
   Wishlist data + render
───────────────────────────── */
function getLandingI18n() {
  const el = document.getElementById('landing-i18n');
  if (!el) return {};
  try {
    return JSON.parse(el.textContent);
  } catch {
    return {};
  }
}

function getLandingWishlist() {
  const el = document.getElementById('landing-wishlist');
  if (!el) return [];
  try {
    const data = JSON.parse(el.textContent);
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

let wishlistCache = null;
function getWishlist() {
  if (wishlistCache === null) wishlistCache = getLandingWishlist();
  return wishlistCache;
}

function renderWishlist() {
  const container = document.getElementById('wishlist-items');
  if (!container) return;
  const i = getWishlistI18n();
  const list = getWishlist();
  const countEl = document.getElementById('wishlist-count');

  if (countEl) {
    if (list.length) {
      countEl.textContent = list.length === 1
        ? (i.savedOne || '1 restaurant saved')
        : `${list.length} ${i.savedMany || 'restaurants saved'}`;
      countEl.hidden = false;
    } else {
      countEl.hidden = true;
      countEl.textContent = '';
    }
  }

  if (!list.length) {
    container.innerHTML = `
      <div class="wishlist-empty">
        <span class="wishlist-empty__icon" aria-hidden="true"><i data-lucide="heart"></i></span>
        <p class="wishlist-empty__title">${i.wishlistEmpty || 'Nothing saved yet'}</p>
        <p class="wishlist-empty__hint">${i.wishlistHint || 'Tap ♥ on a restaurant to save it'}</p>
      </div>`;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = list.map((r) => `
    <a href="${r.url || '#'}" class="wishlist-item">
      <div class="wishlist-item__body">
        <span class="wishlist-item__name">${r.name}</span>
        <span class="wishlist-item__meta">${[r.cuisine, r.city].filter(Boolean).join(' · ')}</span>
      </div>
      ${r.rating ? `<span class="wishlist-item__rating">★ ${r.rating}</span>` : ''}
    </a>
  `).join('');
}

function removeWishlist(index) {
  getWishlist().splice(index, 1);
  renderWishlist();
}

/* ─────────────────────────────
   AI Chat
───────────────────────────── */
const aiMessages = [];

async function sendAIMessage() {
  const input = document.getElementById('ai-input');
  const msg   = input.value.trim();
  if (!msg) return;
  input.value = '';
  aiMessages.push({ role: 'user', content: msg });
  renderChat();

  const chat = document.getElementById('ai-chat');
  const typing = document.createElement('div');
  typing.id = 'typing-indicator';
  typing.className = 'flex justify-start mb-3';
  typing.innerHTML = `<div class="px-4 py-2.5 rounded-2xl rounded-bl-sm bg-gray-100 text-gray-500 text-sm"><span class="typing-dots">●●●</span></div>`;
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
        messages: aiMessages,
      }),
    });
    const data  = await res.json();
    const reply = data.content?.[0]?.text || 'عذراً، حدث خطأ. / Sorry, something went wrong.';
    aiMessages.push({ role: 'assistant', content: reply });
  } catch {
    aiMessages.push({ role: 'assistant', content: 'عذراً، تحقق من اتصالك. / Please check your connection.' });
  }

  document.getElementById('typing-indicator')?.remove();
  renderChat();
}

function renderChat() {
  const chat = document.getElementById('ai-chat');
  if (!chat) return;
  chat.innerHTML = `
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

document.getElementById('ai-input')?.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendAIMessage(); }
});

/* ─────────────────────────────
   Leaflet Map
───────────────────────────── */
let yummMap = null;
let searchMarker = null;

function getMapRestaurants() {
  const el = document.getElementById('landing-map-restaurants');
  if (!el) return [];
  try {
    const data = JSON.parse(el.textContent);
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

function initMap() {
  if (yummMap) { yummMap.invalidateSize(); return; }
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
  window.YummMap.addBaseTileLayer(yummMap);

  const redIcon = L.divIcon({
    html: `<div style="background:#B5451B;width:32px;height:32px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>`,
    iconSize: [32, 32], iconAnchor: [16, 32], popupAnchor: [0, -36], className: '',
  });

  const restaurants = getMapRestaurants();
  restaurants.forEach(r => {
    const popup = r.url
      ? `<b>${r.name}</b><br><span style="color:#666;font-size:12px">${r.desc || ''}</span><br><a href="${r.url}" style="color:#B5451B;font-size:12px;font-weight:600">View →</a>`
      : `<b>${r.name}</b><br><span style="color:#666;font-size:12px">${r.desc || ''}</span>`;
    L.marker([r.lat, r.lng], { icon: redIcon })
      .addTo(yummMap)
      .bindPopup(popup, { maxWidth: 220 });
  });

  if (restaurants.length) {
    const bounds = L.latLngBounds(restaurants.map(r => [r.lat, r.lng]));
    yummMap.fitBounds(bounds.pad(0.15));
  }
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
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`,
      { headers: { 'Accept-Language': window.YummMap.mapSearchLanguage() } },
    );
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

document.getElementById('map-search-input')?.addEventListener('keydown', e => {
  if (e.key === 'Enter') searchMapLocation();
});

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
  initWishlistAjax();
  updateWishlistFabBadge();

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
  function showError(field, msg) {
    field.classList.add('border-red-500');
    const err = document.createElement('p');
    err.className = 'text-red-400 text-xs mt-1 field-error';
    err.textContent = msg;
    field.parentElement.appendChild(err);
  }
  function clearErrors() {
    document.querySelectorAll('.field-error').forEach(e => e.remove());
    form.querySelectorAll('input,textarea').forEach(f => f.classList.remove('border-red-500'));
  }
});