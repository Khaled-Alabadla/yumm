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
