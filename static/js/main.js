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

function submitSiteLanguage(code) {
    const form = document.getElementById('lang-form');
    if (!form) return false;
    const input = form.querySelector('input[name="language"]');
    if (input) input.value = code;
    form.submit();
    return true;
}

/* ─────────────────────────────
   Language toggle (Django set_language)
───────────────────────────── */
function toggleLang() {
    const lang = document.documentElement.lang?.startsWith('ar') ? 'ar' : 'en';
    submitSiteLanguage(lang === 'ar' ? 'en' : 'ar');
}

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

function setLang(flag, name, code) {
    document.getElementById('lang-flag').textContent = flag;
    document.getElementById('lang-name').textContent = name;
    document.getElementById('lang-drop').classList.add('hidden');

    if (code === 'ar' || code === 'en') {
        submitSiteLanguage(code);
    }
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
  const linehVal = document.getElementById('lineh-val');
  if (!linehVal) return;
  if (lh === 0) {
    document.body.style.lineHeight = '';
    linehVal.textContent = defaultFontLabel();
  } else {
    document.body.style.lineHeight = (1.5 + lh).toFixed(1);
    linehVal.textContent = (1.5 + lh).toFixed(1);
  }
}

/* ─────────────────────────────
   Letter spacing
───────────────────────────── */
let ls = 0;

function changeLetterS(d) {
  ls = Math.round((ls + d) * 100) / 100;
  ls = Math.max(-0.1, Math.min(0.3, ls));
  const lettersVal = document.getElementById('letters-val');
  if (!lettersVal) return;
  if (ls === 0) {
    document.body.style.letterSpacing = '';
    lettersVal.textContent = defaultFontLabel();
  } else {
    document.body.style.letterSpacing = ls + 'em';
    lettersVal.textContent = ls + 'em';
  }
}

/* ─────────────────────────────
   Content scaling
───────────────────────────── */
let scaleVal = 100;

function changeScale(d) {
  scaleVal = Math.max(70, Math.min(150, scaleVal + d));
  const main = document.getElementById('main');
  const scaleValEl = document.getElementById('scale-val');
  if (main) main.style.zoom = scaleVal === 100 ? '' : (scaleVal / 100);
  if (scaleValEl) {
    scaleValEl.textContent = scaleVal === 100 ? defaultFontLabel() : scaleVal + '%';
  }
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

  fs = 16; html.style.fontSize = '16px';
  lh = 0;  ls = 0;  scaleVal = 100;

    const def = defaultFontLabel();
    const fontVal = document.getElementById('font-val');
    if (fontVal) fontVal.textContent = def;
    const linehVal = document.getElementById('lineh-val');
    if (linehVal) linehVal.textContent = def;
    const lettersVal = document.getElementById('letters-val');
    if (lettersVal) lettersVal.textContent = def;
    const scaleValEl = document.getElementById('scale-val');
    if (scaleValEl) scaleValEl.textContent = def;

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
  const viewLabel = document.getElementById('map-search-input')?.dataset.viewLabel || 'View';
  restaurants.forEach(r => {
    const popup = r.url
      ? `<b>${r.name}</b><br><span style="color:#666;font-size:12px">${r.desc || ''}</span><br><a href="${r.url}" style="color:#B5451B;font-size:12px;font-weight:600">${viewLabel} →</a>`
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
  const input = document.getElementById('map-search-input');
  const query = input?.value.trim();
  if (!query || !yummMap) return;
  const notFound = input.dataset.notFound || 'Location not found. Try a different search.';
  const searchFailed = input.dataset.searchFailed || 'Search failed. Please try again.';
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`,
      { headers: { 'Accept-Language': window.YummMap.mapSearchLanguage() } },
    );
    const data = await res.json();
    if (!data.length) { alert(notFound); return; }
    const { lat, lon, display_name } = data[0];
    if (searchMarker) yummMap.removeLayer(searchMarker);
    searchMarker = L.marker([lat, lon]).addTo(yummMap)
      .bindPopup(`<b>🔍 ${query}</b><br><span style="color:#666;font-size:11px">${display_name.substring(0, 60)}...</span>`)
      .openPopup();
    yummMap.flyTo([lat, lon], 13, { duration: 1.2 });
  } catch { alert(searchFailed); }
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

  const form = document.querySelector('.yumm-form-stack[method="post"]');
  if (!form || !form.dataset.errorNameRequired) return;
  form.addEventListener('submit', e => {
    const name    = form.querySelector('[name="name"]');
    const email   = form.querySelector('[name="email"]');
    const message = form.querySelector('[name="message"]');
    clearErrors();
    let valid = true;
    if (!name.value.trim()) {
      showError(name, form.dataset.errorNameRequired);
      valid = false;
    }
    if (!email.value.trim() || !email.value.includes('@')) {
      showError(email, form.dataset.errorEmailInvalid);
      valid = false;
    }
    if (!message.value.trim() || message.value.trim().length < 10) {
      showError(message, form.dataset.errorMessageShort);
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
    form.querySelectorAll('input,textarea').forEach(f => f.classList.remove('border-red-500'));
  }
});