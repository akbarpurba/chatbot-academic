const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messagesArea = document.getElementById("messagesArea");
const typingIndicator = document.getElementById("typingIndicator");
const themeToggle = document.getElementById("themeToggle");

// ==================== DARK MODE ====================
// Cek preferensi dari localStorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
  document.body.classList.add('dark-mode');
  updateThemeIcon();
}

function updateThemeIcon() {
  const isDark = document.body.classList.contains('dark-mode');
  const icon = themeToggle.querySelector('i');
  if (isDark) {
    icon.classList.remove('fa-moon');
    icon.classList.add('fa-sun');
  } else {
    icon.classList.remove('fa-sun');
    icon.classList.add('fa-moon');
  }
}

themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  const isDark = document.body.classList.contains('dark-mode');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  updateThemeIcon();
});

// ==================== CHAT FUNCTIONS ====================
input.addEventListener("input", () => {
  sendBtn.disabled = input.value.trim() === "";
});

input.addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

sendBtn.addEventListener("click", sendMessage);

document.querySelectorAll(".chip").forEach((btn) => {
  btn.addEventListener("click", () => {
    input.value = btn.dataset.query;
    sendMessage();
  });
});

function decodeHTML(html) {
  const txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}

function formatBotMessage(text) {
  let formatted = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
  
  formatted = formatted.replace(/\n/g, "<br>");
  formatted = formatted.replace(/•/g, '<span class="bullet-point">•</span>');
  formatted = formatted.replace(/(\d+)\./g, '<span class="number-point">$1.</span>');
  
  return formatted;
}

async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";
  sendBtn.disabled = true;

  showTyping();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    hideTyping();

    const decodedReply = decodeHTML(data.reply);
    const formattedReply = formatBotMessage(decodedReply);
    addMessage(formattedReply, "bot");
  } catch (err) {
    hideTyping();
    addMessage("Maaf, terjadi kesalahan. Silakan coba lagi.", "bot");
  }
}

function addMessage(text, sender) {
  const row = document.createElement("div");
  row.className = `message-row ${sender}-message`;

  if (sender === "bot") {
    row.innerHTML = `
      <div class="bot-avatar-mini">
        <div class="avatar-sm">🤖</div>
      </div>
      <div class="message-bubble">
        <div class="message-text">${text}</div>
        <button class="copy-msg-btn" title="Salin">
          <i class="fa-regular fa-copy"></i>
        </button>
      </div>
    `;
  } else {
    row.innerHTML = `
      <div class="message-bubble">
        <div class="message-text">${text}</div>
        <button class="copy-msg-btn" title="Salin">
          <i class="fa-regular fa-copy"></i>
        </button>
      </div>
    `;
  }

  messagesArea.appendChild(row);
  messagesArea.scrollTop = messagesArea.scrollHeight;

  const copyBtn = row.querySelector(".copy-msg-btn");
  if (copyBtn) {
    const icon = copyBtn.querySelector("i");
    copyBtn.addEventListener("click", () => {
      const plainText = row.querySelector(".message-text").innerText;
      navigator.clipboard.writeText(plainText).then(() => {
        icon.classList.remove("fa-copy");
        icon.classList.add("fa-check");
        copyBtn.classList.add("copied");
        setTimeout(() => {
          icon.classList.remove("fa-check");
          icon.classList.add("fa-copy");
          copyBtn.classList.remove("copied");
        }, 1500);
      });
    });
  }
}

function showTyping() {
  typingIndicator.style.display = "flex";
  messagesArea.scrollTop = messagesArea.scrollHeight;
}

function hideTyping() {
  typingIndicator.style.display = "none";
}