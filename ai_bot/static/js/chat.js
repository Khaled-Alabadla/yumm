const chatEl        = document.getElementById('chatMessages');
const inputEl       = document.getElementById('chatInput');


function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function sendSuggestion(text) {
    inputEl.value = text;
    sendMessage();
}


function scroll() {
    chatEl.scrollTop = chatEl.scrollHeight;
}
