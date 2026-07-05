const chatEl = document.getElementById('chatMessages');
const inputEl = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

let history = [];
let isLoading = false;
let sessionId = null;

const previousMessagesScript = document.getElementById("previousMessages");
const previousMessages = previousMessagesScript
    ? JSON.parse(previousMessagesScript.textContent)
    : [];

function renderPreviousMessages() {
    if (!previousMessages.length) return;

    document.getElementById("welcomeMsg")?.remove();

    previousMessages.forEach(msg => {
        msg.role === "user"
            ? appendUser(msg.content)
            : appendAI(msg.content);

        history.push(msg);
    });
}

function getCookie(name) {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
}

function escapeHTML(str) {
    return str.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function reloadIcons() {
    if (window.lucide) lucide.createIcons();
}

function appendUser(text) {
    document.getElementById('welcomeMsg')?.remove();

    const el = document.createElement('div');
    el.className = 'flex gap-3 items-start flex-row-reverse';

    el.innerHTML = `
        <div class="w-8 h-8 rounded-xl flex items-center justify-center mt-1"
            style="background:#B5451B">
            <i data-lucide="user" class="w-4 h-4 text-white"></i>
        </div>

        <div class="rounded-2xl px-4 py-3 max-w-xl text-sm"
            style="background:#B5451B;color:white">
            ${escapeHTML(text).replace(/\n/g, "<br>")}
        </div>
    `;

    chatEl.appendChild(el);
    reloadIcons();
    chatEl.scrollTop = chatEl.scrollHeight;
}

function appendAI(text) {
    const el = document.createElement('div');
    el.className = 'flex gap-3 items-start';

    el.innerHTML = `
        <div class="w-8 h-8 rounded-xl flex items-center justify-center mt-1"
            style="background:rgba(181,69,27,0.15)">
            <i data-lucide="bot" class="w-4 h-4" style="color:#B5451B"></i>
        </div>

        <div class="rounded-2xl px-4 py-3 max-w-xl text-sm"
            style="background:var(--card);border:1px solid var(--border)">
            ${escapeHTML(text).replace(/\n/g, "<br>")}
        </div>
    `;

    chatEl.appendChild(el);
    reloadIcons();
    chatEl.scrollTop = chatEl.scrollHeight;
}

function appendRestaurantCards(htmlList) {
    if (!Array.isArray(htmlList) || htmlList.length === 0) return;

    const wrapper = document.createElement("div");
    wrapper.className = "flex flex-col gap-3 max-w-xl ml-11";

    htmlList.forEach(html => {
        const container = document.createElement("div");
        container.innerHTML = html;

        const card = container.firstElementChild;
        if (card) wrapper.appendChild(card);
    });

    chatEl.appendChild(wrapper);
    reloadIcons();
    chatEl.scrollTop = chatEl.scrollHeight;
}

function showTyping() {
    const el = document.createElement('div');
    el.id = 'typingIndicator';
    el.className = 'flex gap-3 items-start';

    el.innerHTML = `
        <div class="w-8 h-8 rounded-xl flex items-center justify-center"
            style="background:rgba(181,69,27,0.15)">
            <i data-lucide="bot" class="w-4 h-4"></i>
        </div>

        <div class="px-4 py-3 text-sm"
            style="background:var(--card);border:1px solid var(--border)">
            typing...
        </div>
    `;

    chatEl.appendChild(el);
    reloadIcons();
    chatEl.scrollTop = chatEl.scrollHeight;
}

function removeTyping() {
    document.getElementById('typingIndicator')?.remove();
}

async function sendMessage() {
    const msg = inputEl.value.trim();
    if (!msg || isLoading) return;

    isLoading = true;
    sendBtn.disabled = true;

    inputEl.value = '';

    appendUser(msg);
    history.push({ role: 'user', content: msg });

    showTyping();

    try {
        const res = await fetch('/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                message: msg,
                history: history.slice(-10),
                session_id: sessionId,
            }),
        });

        const data = await res.json();

        removeTyping();

        sessionId = data.session_id || sessionId;

        appendAI(data.reply || "No response");

        if (data.restaurants_html?.length) {
            appendRestaurantCards(data.restaurants_html);
        }

        history.push({ role: 'assistant', content: data.reply });

    } catch (err) {
        removeTyping();
        appendAI("Something went wrong 😓");
    }

    isLoading = false;
    sendBtn.disabled = false;
    inputEl.focus();
}
function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

renderPreviousMessages();