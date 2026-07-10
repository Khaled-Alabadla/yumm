const chatEl = document.getElementById('chatMessages');
const inputEl = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatConfigEl = document.getElementById('chatConfig');
const chatI18n = {
    errorReply: chatConfigEl?.dataset.errorReply || 'Sorry, I could not process that.',
    errorNetwork: chatConfigEl?.dataset.errorNetwork || 'Sorry, something went wrong. Please try again.',
    uncertainPrefix: chatConfigEl?.dataset.uncertainPrefix || "I'm not entirely sure I understood — here's my best answer:",
};
let history = [];
let isLoading = false;
let sessionId = null;
let lastRestaurants = [];

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function sendSuggestion(text) {
    if (!inputEl || !text) return;
    inputEl.value = text;
    autoResize(inputEl);
    inputEl.focus();
}

function bindSuggestionChips() {
    document.querySelectorAll('.chat-suggestion').forEach((btn) => {
        btn.addEventListener('click', () => {
            const text = btn.dataset.suggestion || btn.textContent.trim();
            sendSuggestion(text);
        });
    });
}


function scroll() {
    chatEl.scrollTop = chatEl.scrollHeight;
}

const bounceStyle = document.createElement('style');
bounceStyle.textContent = `@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-5px)}}`;
document.head.appendChild(bounceStyle);



function getCookie(name) {
    const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : '';
}



function reloadIcons() {
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function cloneTemplate(id) {
    return document.getElementById(id).content.cloneNode(true);
}


function loadPreviousMessages(messages) {
    if (!messages || !messages.length) return;
    document.getElementById('welcomeMsg')?.remove();
    messages.forEach(m => {
        if (m.role === 'user') appendUser(m.content, false);
        else appendAI(m.content, false);
    });
    scroll();
}
function initChat() {
    const configEl = document.getElementById('chatConfig');
    if (configEl && configEl.dataset.sessionId) {
        sessionId = configEl.dataset.sessionId;
    }

    const prevMsgsEl = document.getElementById('previousMessages');
    if (!prevMsgsEl) return;

    try {
        const messages = JSON.parse(prevMsgsEl.textContent);
        if (messages && messages.length) {
            loadPreviousMessages(messages);
            history = messages.map(m => ({ role: m.role, content: m.content }));
        }
    } catch (e) {
        console.error('Failed to restore previous messages:', e);
    }
}

initChat();
bindSuggestionChips();

function appendUser(text, doScroll = true) {
    document.getElementById('welcomeMsg')?.remove();
    const el = document.createElement('div');
    el.className = 'flex gap-3 items-start flex-row-reverse';
    el.innerHTML = `
        <div class="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1"
            style="background:#B5451B">
            <i data-lucide="user" class="w-4 h-4 text-white"></i>
        </div>
        <div class="rounded-2xl rounded-tr-sm px-4 py-3 max-w-xl text-sm leading-relaxed text-white"
            style="background:#B5451B"></div>`;
    el.querySelector('div:last-child').textContent = text;
    chatEl.appendChild(el);
    reloadIcons();
    if (doScroll) scroll();
}

function appendAI(text, doScroll = true) {
    const el = document.createElement('div');
    el.className = 'flex gap-3 items-start';
    el.innerHTML = `
        <div class="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1"
            style="background:rgba(181,69,27,0.15)">
            <i data-lucide="bot" class="w-4 h-4" style="color:#B5451B"></i>
        </div>
        <div class="rounded-2xl rounded-tl-sm px-4 py-3 max-w-xl text-[13.5px] leading-[1.7]"
            style="background:var(--card);border:1px solid var(--border);color:var(--text-primary);white-space:pre-line"></div>`;
    el.querySelector('div:last-child').textContent = text;
    chatEl.appendChild(el);
    reloadIcons();
    if (doScroll) scroll();
}

function appendRestaurantCards(restaurantsHtml) {
    if (!restaurantsHtml || !restaurantsHtml.length) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'flex flex-col gap-3 max-w-xl ml-11 mt-1';

    restaurantsHtml.forEach(html => {
        const div = document.createElement('div');
        div.innerHTML = html.trim();
        if (div.firstElementChild) {
            wrapper.appendChild(div.firstElementChild);
        }
    });

    chatEl.appendChild(wrapper);
    reloadIcons();
    scroll();
}

function showTyping() {
    const el = document.createElement('div');
    el.id = 'typingIndicator';
    el.className = 'flex gap-3 items-start';
    el.innerHTML = `
        <div class="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1"
            style="background:rgba(181,69,27,0.15)">
            <i data-lucide="bot" class="w-4 h-4" style="color:#B5451B"></i>
        </div>
        <div class="rounded-2xl rounded-tl-sm px-4 py-3 text-sm"
            style="background:var(--card);border:1px solid var(--border);color:var(--text-secondary)">
            <span style="display:inline-flex;gap:4px">
                <span style="animation:bounce 1.2s infinite 0ms">●</span>
                <span style="animation:bounce 1.2s infinite 200ms">●</span>
                <span style="animation:bounce 1.2s infinite 400ms">●</span>
            </span>
        </div>`;
    chatEl.appendChild(el);
    reloadIcons();
    scroll();
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
    inputEl.style.height = 'auto';

    appendUser(msg);
    history.push({ role: 'user', content: msg });
    showTyping();

    try {
        const res = await fetch(chatConfigEl?.dataset.url || '/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                message: msg,
                history: history.slice(-6),
                session_id: sessionId,
                last_restaurants: lastRestaurants.map(r => r.id),
            }),
        });

        const data = await res.json();
        const reply = data.reply || chatI18n.errorReply;

        removeTyping();

        const prefix = (data.confidence && data.confidence < 0.6)
            ? chatI18n.uncertainPrefix + '\n\n'
            : '';
        appendAI(prefix + reply);

        if (data.restaurants_html && data.restaurants_html.length) {
            appendRestaurantCards(data.restaurants_html);
            lastRestaurants = data.restaurants || [];
        }

        if (data.session_id) sessionId = data.session_id;

        history.push({ role: 'assistant', content: reply });

    } catch {
        removeTyping();
        appendAI(chatI18n.errorNetwork);
    }

    isLoading = false;
    sendBtn.disabled = false;
    inputEl.focus();
}