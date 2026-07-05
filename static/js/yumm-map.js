/**
 * Shared Leaflet base map — Latin/Arabic labels (no Hebrew tile text).
 */
(function (global) {
  'use strict';

  const TILE_URL =
    'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png';

  const TILE_OPTIONS = {
    maxZoom: 20,
    subdomains: 'abcd',
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> ' +
      '&copy; <a href="https://carto.com/attributions">CARTO</a>',
  };

  function addBaseTileLayer(map) {
    if (typeof L === 'undefined') return null;
    return L.tileLayer(TILE_URL, TILE_OPTIONS).addTo(map);
  }

  /** Prefer Arabic or English in geocoder results (not Hebrew). */
  function mapSearchLanguage() {
    const lang = (document.documentElement.lang || 'en').toLowerCase();
    return lang.startsWith('ar') ? 'ar,en' : 'en,ar';
  }

  global.YummMap = {
    addBaseTileLayer,
    mapSearchLanguage,
  };
})(window);
