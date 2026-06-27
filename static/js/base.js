function updateClock() {
    const now = new Date();
    document.getElementById('navTime').textContent =
        now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    document.getElementById('navDate').textContent =
        now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
}
updateClock();
setInterval(updateClock, 1000);

function toggleTheme() {
    const html = document.documentElement;

    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }

    syncThemeIcon();
}

function syncThemeIcon() {
    const isDark = document.documentElement.classList.contains('dark');
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = isDark ? 'fa-solid fa-sun text-sm' : 'fa-solid fa-moon text-sm';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
    }

    syncThemeIcon();
});


function toggleSidebar() {
    const sidebar = document.getElementById('mobileSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    const isHidden = sidebar.classList.contains('translate-x-full');

    if (isHidden) {
        sidebar.classList.remove('translate-x-full');
        overlay.classList.remove('hidden');
    } else {
        sidebar.classList.add('translate-x-full');
        overlay.classList.add('hidden');
    }
}


document.addEventListener("click", function (e) {
    const menu = document.getElementById("userMenu");
    const button = e.target.closest("[onclick='toggleUserMenu()']");

    if (button) {
        menu.classList.toggle("hidden");
    } else if (!e.target.closest("#userMenu")) {
        menu.classList.add("hidden");
    }
});

function togglePass(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);

  if (!input || !icon) return;

  if (input.type === "password") {
    input.type = "text";
    icon.className = "fa-solid fa-eye-slash text-sm";
  } else {
    input.type = "password";
    icon.className = "fa-solid fa-eye text-sm";
  }
}