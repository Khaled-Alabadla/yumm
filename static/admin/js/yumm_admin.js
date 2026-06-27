/**
 * Yumm Admin — lock Bootstrap 5 to light mode (Jazzmin 3.x).
 */
(function () {
  "use strict";

  function applyLight() {
    localStorage.setItem("jazzmin-theme-mode", "light");
    localStorage.removeItem("jazzmin-theme");
    document.documentElement.setAttribute("data-bs-theme", "light");
  }

  function applyRtl() {
    var html = document.documentElement;
    var lang = (html.getAttribute("lang") || "").toLowerCase();
    var rtl =
      html.getAttribute("dir") === "rtl" ||
      lang.indexOf("ar") === 0 ||
      document.body.classList.contains("yumm-rtl");
    if (rtl) {
      html.setAttribute("dir", "rtl");
      document.body.classList.add("yumm-rtl");
    }
  }

  applyLight();
  applyRtl();
  document.addEventListener("DOMContentLoaded", function () {
    applyLight();
    applyRtl();
  });
  window.addEventListener("load", function () {
    applyLight();
    applyRtl();
  });

  /* Block theme/mode selectors if Jazzmin adds them later */
  document.addEventListener("DOMContentLoaded", function () {
    var modeSelect = document.getElementById("jazzmin-mode-select");
    if (modeSelect) {
      modeSelect.value = "light";
      modeSelect.disabled = true;
    }

    /* Align changelist filter selects in one row (after Jazzmin Select2 init) */
    if (typeof jQuery !== "undefined") {
      jQuery(function ($) {
        function fixFilterSelects() {
          $("#changelist-search .select2-container").css({
            width: "148px",
            "min-width": "148px",
            "max-width": "148px",
          });
        }
        fixFilterSelects();
        setTimeout(fixFilterSelects, 100);
      });
    }

    var brandLogo = document.querySelector("#jazzy-logo .brand-image");
    if (brandLogo && window.YUMM_BRAND_LOGO) {
      brandLogo.src = window.YUMM_BRAND_LOGO;
      brandLogo.classList.remove("opacity-75", "shadow", "img-circle");
      brandLogo.classList.add("yumm-brand-logo");
    }

    /* RTL sidebar — override AdminLTE LTR off-canvas margins after toggle */
    function fixRtlSidebar() {
      var rtl =
        document.documentElement.getAttribute("dir") === "rtl" ||
        document.body.classList.contains("yumm-rtl");
      if (!rtl) {
        return;
      }

      var isMobile = window.matchMedia("(max-width: 991.98px)").matches;
      var isOpen = document.body.classList.contains("sidebar-open");
      var isCollapsed =
        document.body.classList.contains("sidebar-collapse") &&
        !document.body.classList.contains("sidebar-mini");
      var sidebarWidth =
        getComputedStyle(document.documentElement).getPropertyValue("--lte-sidebar-width").trim() ||
        "250px";
      var hiddenMargin = "calc(" + sidebarWidth + " * -1)";

      document.querySelectorAll(".app-sidebar").forEach(function (sidebar) {
        sidebar.style.marginLeft = "0";
        sidebar.style.left = "auto";
        sidebar.style.right = isMobile ? "0" : "";

        if (isMobile) {
          sidebar.style.marginRight = isOpen ? "0" : hiddenMargin;
        } else if (isCollapsed) {
          sidebar.style.marginRight = hiddenMargin;
        } else {
          sidebar.style.marginRight = "0";
        }
      });
    }

    fixRtlSidebar();
    document.addEventListener("click", function (event) {
      if (event.target.closest('[data-lte-toggle="sidebar"]') || event.target.closest(".sidebar-overlay")) {
        window.setTimeout(fixRtlSidebar, 0);
      }
    });
    window.addEventListener("resize", fixRtlSidebar);
  });
})();
