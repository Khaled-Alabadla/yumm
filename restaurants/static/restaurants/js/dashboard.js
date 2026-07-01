/** Restaurant dashboard — modal helpers & AJAX menu delete */

function getCsrfToken() {
  var meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.getAttribute("content");

  var match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

function getPageDir() {
  if (window.RD_PAGE && window.RD_PAGE.dir) {
    return window.RD_PAGE.dir;
  }
  return document.documentElement.dir || "ltr";
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function getMenuI18n() {
  if (window.RD_MENU_I18N && window.RD_MENU_I18N.deleteTitle) {
    return window.RD_MENU_I18N;
  }

  var jsonNode = document.getElementById("rd-menu-i18n");
  if (jsonNode && jsonNode.textContent) {
    try {
      window.RD_MENU_I18N = JSON.parse(jsonNode.textContent);
      if (window.RD_MENU_I18N.deleteTitle) {
        return window.RD_MENU_I18N;
      }
    } catch (error) {
      /* use backup below */
    }
  }

  var cfg = document.getElementById("rd-menu-page-config");
  if (cfg && cfg.dataset) {
    window.RD_MENU_I18N = {
      deleteTitle: cfg.dataset.deleteTitle,
      deleteText: cfg.dataset.deleteText,
      confirmDelete: cfg.dataset.confirmDelete,
      cancel: cfg.dataset.cancel,
      deleted: cfg.dataset.deleted,
      deleteFailed: cfg.dataset.deleteFailed,
      ok: cfg.dataset.ok,
    };
    return window.RD_MENU_I18N;
  }

  return {
    deleteTitle: "Delete menu item?",
    deleteText: "This action cannot be undone.",
    confirmDelete: "Yes, delete",
    cancel: "Cancel",
    deleted: "Deleted!",
    deleteFailed: "Could not delete this item.",
    ok: "OK",
  };
}

function openMenuModal(id) {
  var modal = document.getElementById("menu-modal-" + id);
  if (modal) {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
    if (window.lucide) lucide.createIcons();
  }
}

function closeMenuModal(id) {
  var modal = document.getElementById("menu-modal-" + id);
  if (modal) {
    modal.classList.add("hidden");
    document.body.style.overflow = "";
  }
}

function swalBaseConfig() {
  var dir = getPageDir();
  var isRtl = dir === "rtl";

  return {
    customClass: {
      popup: "rd-swal-popup " + (isRtl ? "rd-swal-popup--rtl" : "rd-swal-popup--ltr"),
      title: "rd-swal-title",
      htmlContainer: "rd-swal-text",
      actions: "rd-swal-actions",
      confirmButton: "rd-swal-confirm",
      cancelButton: "rd-swal-cancel",
    },
    buttonsStyling: false,
    reverseButtons: isRtl,
  };
}

function buildDeleteDialogHtml(itemName, warningText) {
  var dir = getPageDir();

  if (!itemName) {
    return (
      '<div dir="' +
      dir +
      '" class="rd-swal-body"><p class="rd-swal-warning">' +
      escapeHtml(warningText) +
      "</p></div>"
    );
  }

  return (
    '<div dir="' +
    dir +
    '" class="rd-swal-body"><p class="rd-swal-item-name">' +
    escapeHtml(itemName) +
    '</p><p class="rd-swal-warning">' +
    escapeHtml(warningText) +
    "</p></div>"
  );
}

function toggleMenuEmptyState() {
  var list = document.getElementById("menu-items-list");
  var empty = document.getElementById("menu-empty-state");
  if (!list || !empty) return;

  var hasItems = list.querySelectorAll("[data-item-id]").length > 0;
  empty.classList.toggle("hidden", hasItems);
  list.classList.toggle("hidden", !hasItems);
}

async function deleteMenuItem(button) {
  if (!window.Swal) return;

  var i18n = getMenuI18n();
  var itemName = button.dataset.name || "";
  var itemId = button.dataset.itemId;
  var url = button.dataset.url;
  var deleteTitle = i18n.deleteTitle || "Delete menu item?";
  var deleteText = i18n.deleteText || "This action cannot be undone.";

  var result = await Swal.fire(
    Object.assign({}, swalBaseConfig(), {
      icon: "warning",
      title: deleteTitle,
      html: buildDeleteDialogHtml(itemName, deleteText),
      showCancelButton: true,
      confirmButtonText: i18n.confirmDelete || "Yes, delete",
      cancelButtonText: i18n.cancel || "Cancel",
      focusCancel: true,
    })
  );

  if (!result.isConfirmed) return;

  button.disabled = true;

  try {
    var response = await fetch(url, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCsrfToken(),
      },
      credentials: "same-origin",
    });

    var data;
    try {
      data = await response.json();
    } catch (parseError) {
      throw new Error(i18n.deleteFailed);
    }

    if (!response.ok || !data.success) {
      throw new Error(data.message || i18n.deleteFailed);
    }

    var card = document.querySelector('[data-item-id="' + itemId + '"]');
    if (card) card.remove();

    var editModal = document.getElementById("menu-modal-edit-" + itemId);
    if (editModal) editModal.remove();

    toggleMenuEmptyState();

    await Swal.fire(
      Object.assign({}, swalBaseConfig(), {
        icon: "success",
        title: i18n.deleted,
        text: data.message,
        timer: 1600,
        showConfirmButton: false,
      })
    );
  } catch (error) {
    button.disabled = false;
    await Swal.fire(
      Object.assign({}, swalBaseConfig(), {
        icon: "error",
        title: i18n.deleteFailed,
        text: error.message,
        confirmButtonText: i18n.ok || i18n.cancel,
      })
    );
  }
}

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    document.querySelectorAll(".rd-modal:not(.hidden)").forEach(function (modal) {
      modal.classList.add("hidden");
    });
    document.body.style.overflow = "";
  }
});

document.addEventListener("DOMContentLoaded", function () {
  if (window.lucide) lucide.createIcons();

  document.querySelectorAll(".rd-modal:not(.hidden)").forEach(function () {
    document.body.style.overflow = "hidden";
  });

  document.querySelectorAll(".rd-menu-delete-btn").forEach(function (button) {
    button.addEventListener("click", function () {
      deleteMenuItem(button);
    });
  });
});
