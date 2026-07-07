/**
 * Public restaurant pages — map, wishlist, tabs, review stars.
 */

(function () {
  'use strict';

  const MAP_CENTER = [31.9, 35.25];
  const MAP_DEFAULT_ZOOM = 8;

  function parseCoord(value) {
    if (value === null || value === undefined || value === '') return NaN;
    return parseFloat(String(value).trim().replace(',', '.'));
  }

  function getMapData() {
    const el = document.getElementById('rp-map-data');
    if (!el) return [];
    try {
      let data = JSON.parse(el.textContent);
      if (typeof data === 'string') {
        data = JSON.parse(data);
      }
      return Array.isArray(data) ? data : [];
    } catch {
      return [];
    }
  }

  function getMapI18n() {
    const el = document.getElementById('rp-map-i18n');
    if (!el) return { view: 'View', viewRestaurant: 'View Restaurant' };
    try {
      return JSON.parse(el.textContent);
    } catch {
      return { view: 'View', viewRestaurant: 'View Restaurant' };
    }
  }

  function makeMarker(lat, lng, map, layerGroup, m, i18n) {
    const marker = L.circleMarker([lat, lng], {
      radius: 10,
      fillColor: '#b5451b',
      color: '#ffffff',
      weight: 3,
      fillOpacity: 0.95,
    }).addTo(layerGroup);

    marker.bindPopup(
      `<div class="rp-map-popup"><strong>${m.name}</strong><br>` +
      `<a href="${m.url}" class="rp-map-popup__link">${i18n.viewRestaurant || i18n.view}</a></div>`,
    );
    marker.on('click', () => map.setView([lat, lng], 14, { animate: true }));
    return marker;
  }

  function fitMapToMarkers(map, layerGroup) {
    const layers = layerGroup.getLayers();
    if (!layers.length) {
      map.setView(MAP_CENTER, MAP_DEFAULT_ZOOM);
      return;
    }
    if (layers.length === 1) {
      const latLng = layers[0].getLatLng();
      map.setView(latLng, 14);
      return;
    }
    map.fitBounds(layerGroup.getBounds(), { padding: [48, 48], maxZoom: 13 });
  }

  function initListMap() {
    const container = document.getElementById('rp-list-map');
    if (!container || typeof L === 'undefined') return;

    const markers = getMapData();
    const i18n = getMapI18n();

    const map = L.map(container, {
      scrollWheelZoom: true,
      zoomControl: true,
    }).setView(MAP_CENTER, MAP_DEFAULT_ZOOM);

    if (window.YummMap) {
      window.YummMap.addBaseTileLayer(map);
    }

    const layerGroup = L.layerGroup().addTo(map);

    markers.forEach((m) => {
      const lat = parseCoord(m.lat);
      const lng = parseCoord(m.lng);
      if (Number.isNaN(lat) || Number.isNaN(lng)) return;
      makeMarker(lat, lng, map, layerGroup, m, i18n);
    });

    fitMapToMarkers(map, layerGroup);

    /* Leaflet needs a second layout pass after tiles load */
    map.whenReady(() => {
      fitMapToMarkers(map, layerGroup);
      map.invalidateSize();
    });
    setTimeout(() => {
      fitMapToMarkers(map, layerGroup);
      map.invalidateSize();
    }, 250);
    window.addEventListener('resize', () => map.invalidateSize());
  }

  function initFilterForm() {
    const form = document.getElementById('rp-filter-form');
    if (!form) return;

    form.querySelectorAll('input[name="category"]').forEach((radio) => {
      radio.addEventListener('change', () => form.submit());
    });

    const city = document.getElementById('rp-city');
    if (city) {
      city.addEventListener('change', () => form.submit());
    }
  }

  function initDetailMap() {
    const container = document.getElementById('rp-detail-map');
    if (!container || typeof L === 'undefined') return;

    const lat = parseCoord(container.dataset.lat);
    const lng = parseCoord(container.dataset.lng);
    const name = container.dataset.name || '';
    if (Number.isNaN(lat) || Number.isNaN(lng)) return;

    const map = L.map(container, { scrollWheelZoom: false }).setView([lat, lng], 15);
    if (window.YummMap) {
      window.YummMap.addBaseTileLayer(map);
    }
    L.circleMarker([lat, lng], {
      radius: 10,
      fillColor: '#b5451b',
      color: '#ffffff',
      weight: 3,
      fillOpacity: 0.95,
    }).addTo(map).bindPopup(name);
    setTimeout(() => map.invalidateSize(), 100);
  }

  function getCsrf() {
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
  }

  function initStarInput() {
    const wrap = document.querySelector('.rp-star-input');
    const form = document.getElementById('rp-review-form');
    if (!wrap || !form) return;

    const hidden = form.querySelector('[name="rating"]');
    if (!hidden) return;

    const valEl = wrap.querySelector('.rp-star-input__val');

    function paint(n) {
      wrap.querySelectorAll('.rp-star-input__btn').forEach((btn) => {
        const v = parseInt(btn.dataset.value, 10);
        const icon = btn.querySelector('i');
        if (!icon) return;
        icon.className = v <= n ? 'fa-solid fa-star' : 'fa-regular fa-star';
      });
      if (valEl) valEl.textContent = n;
      hidden.value = n > 0 ? String(n) : '';
    }

    const initial = parseInt(wrap.dataset.rating, 10) || parseInt(hidden.value, 10) || 0;
    paint(initial);

    wrap.querySelectorAll('.rp-star-input__btn').forEach((btn) => {
      btn.addEventListener('click', () => paint(parseInt(btn.dataset.value, 10)));
    });

    form.addEventListener('submit', (e) => {
      const displayVal = parseInt(valEl?.textContent || '0', 10) || 0;
      if (displayVal >= 1) {
        hidden.value = String(displayVal);
      }
      if (parseInt(hidden.value, 10) < 1) {
        e.preventDefault();
        let err = form.querySelector('.rp-review-rating-error');
        if (!err) {
          err = document.createElement('p');
          err.className = 'rp-form-errors rp-review-rating-error';
          wrap.after(err);
        }
        err.textContent = form.dataset.ratingError || 'Please select a star rating.';
        wrap.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });

    if (window.location.search.includes('tab=reviews') && document.querySelector('.rp-messages .fa-circle-exclamation, .rp-messages .fa-circle-check')) {
      form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    if (typeof lucide !== 'undefined') lucide.createIcons();

    initFilterForm();

    if (document.getElementById('rp-list-map')) {
      initListMap();
    } else {
      initDetailMap();
    }

    initStarInput();
    if (typeof initWishlistAjax === 'function') initWishlistAjax();
  });
})();
