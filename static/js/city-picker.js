/**
 * Custom city picker — same UI as the restaurants list filter.
 * Binds to [data-rp-city-picker]; set data-auto-submit="true" to submit the parent form on pick.
 */
(function () {
  function initCityPicker(root) {
    if (!root || root.dataset.bound === '1') return;
    root.dataset.bound = '1';

    const select = root.querySelector('select');
    const trigger = root.querySelector('.rp-city-picker__trigger');
    const menu = root.querySelector('.rp-city-picker__menu');
    const valueEl = root.querySelector('[data-rp-city-value]');
    if (!select || !trigger || !menu || !valueEl) return;

    const autoSubmit = root.dataset.autoSubmit === 'true';

    function isOpen() {
      return root.classList.contains('is-open');
    }

    function closeMenu() {
      root.classList.remove('is-open');
      menu.setAttribute('hidden', '');
      trigger.setAttribute('aria-expanded', 'false');
    }

    function openMenu() {
      root.classList.add('is-open');
      menu.removeAttribute('hidden');
      trigger.setAttribute('aria-expanded', 'true');
      const selected = menu.querySelector('.is-selected');
      if (selected) {
        try {
          selected.scrollIntoView({ block: 'nearest' });
        } catch (_) { /* ignore */ }
      }
    }

    function toggleMenu() {
      if (isOpen()) closeMenu();
      else openMenu();
    }

    function chooseOption(option) {
      if (!option) return;
      const value = option.getAttribute('data-value') || '';
      const label = option.textContent.trim();

      select.value = value;
      valueEl.textContent = label;

      menu.querySelectorAll('.rp-city-picker__option').forEach((el) => {
        const on = el === option;
        el.classList.toggle('is-selected', on);
        el.setAttribute('aria-selected', on ? 'true' : 'false');
      });

      closeMenu();

      if (autoSubmit) {
        const form = root.closest('form');
        if (form) {
          if (typeof form.requestSubmit === 'function') form.requestSubmit();
          else form.submit();
        }
      }
    }

    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleMenu();
    });

    menu.addEventListener('click', (e) => {
      const option = e.target.closest('.rp-city-picker__option');
      if (!option) return;
      e.preventDefault();
      e.stopPropagation();
      chooseOption(option);
    });

    document.addEventListener('click', (e) => {
      if (!isOpen()) return;
      if (root.contains(e.target)) return;
      closeMenu();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen()) {
        closeMenu();
        trigger.focus();
      }
    });
  }

  function initAllCityPickers(scope) {
    const root = scope && scope.querySelector ? scope : document;
    root.querySelectorAll('[data-rp-city-picker]').forEach(initCityPicker);
  }

  window.YummCityPicker = {
    init: initCityPicker,
    initAll: initAllCityPickers,
  };

  document.addEventListener('DOMContentLoaded', () => initAllCityPickers());
})();
