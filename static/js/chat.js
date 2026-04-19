// Dark Mode
const themeToggle = document.getElementById('themeToggle');
const savedTheme = localStorage.getItem('theme');

if (savedTheme === 'dark') {
  document.body.classList.add('dark-mode');
  updateThemeIcon();
}

function updateThemeIcon() {
  if (!themeToggle) return;
  const icon = themeToggle.querySelector('i');
  if (document.body.classList.contains('dark-mode')) {
    icon.classList.remove('fa-moon');
    icon.classList.add('fa-sun');
  } else {
    icon.classList.remove('fa-sun');
    icon.classList.add('fa-moon');
  }
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcon();
  });
}

// ============ CHAT FUNCTIONS ============
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messagesArea = document.getElementById("messagesArea");
const typingIndicator = document.getElementById("typingIndicator");
const troubleshootOptions = document.getElementById("troubleshootOptions");

// FUNCTION SCROLL KE BAWAH
function forceScrollToBottom() {
  if (messagesArea) {
    messagesArea.scrollTop = messagesArea.scrollHeight;
    setTimeout(() => {
      messagesArea.scrollTop = messagesArea.scrollHeight;
    }, 50);
    setTimeout(() => {
      messagesArea.scrollTop = messagesArea.scrollHeight;
    }, 150);
  }
}

// Tampilkan button troubleshooting
function showTroubleshootOptions() {
  if (troubleshootOptions) {
    troubleshootOptions.style.display = "block";
    forceScrollToBottom();
  }
}

function hideTroubleshootOptions() {
  if (troubleshootOptions) {
    troubleshootOptions.style.display = "none";
  }
}

// Event listener untuk button troubleshooting
document.querySelectorAll(".troubleshoot-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const type = btn.dataset.type;
    input.value = type;
    hideTroubleshootOptions();
    sendMessage();
  });
});

if (input) {
  input.addEventListener("input", () => {
    sendBtn.disabled = input.value.trim() === "";
  });

  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}

if (sendBtn) {
  sendBtn.addEventListener("click", sendMessage);
}

// Event listener untuk semua chip termasuk troubleshoot chip
document.querySelectorAll(".chip").forEach((btn) => {
  btn.addEventListener("click", () => {
    const query = btn.dataset.query;
    input.value = query;
    sendMessage();
  });
});

function formatBotMessage(text) {
  let formatted = text;
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  formatted = formatted.replace(/\n/g, '<br>');
  formatted = formatted.replace(/•/g, '<span class="bullet-point">•</span>');
  formatted = formatted.replace(/^(\d+)\.\s/gm, '<span class="number-point">$1.</span> ');
  formatted = formatted.replace(/<br>(\d+)\.\s/g, '<br><span class="number-point">$1.</span> ');
  formatted = formatted.replace(/^([^<br>]+):/gm, '<strong>$1:</strong>');
  return formatted;
}

function decodeHTML(html) {
  const txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
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
    
    // Jika user mengklik "saya mengalami kendala", tampilkan options troubleshooting
    if (message.toLowerCase().includes("kendala") || 
        message.toLowerCase().includes("masalah") ||
        message.toLowerCase() === "saya mengalami kendala") {
      showTroubleshootOptions();
    } else {
      hideTroubleshootOptions();
    }
    
  } catch (err) {
    console.error("Error:", err);
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
    const safeText = escapeHtml(text);
    row.innerHTML = `
      <div class="message-bubble">
        <div class="message-text">${safeText}</div>
        <button class="copy-msg-btn" title="Salin">
          <i class="fa-regular fa-copy"></i>
        </button>
      </div>
    `;
  }

  messagesArea.appendChild(row);
  forceScrollToBottom();

  const copyBtn = row.querySelector(".copy-msg-btn");
  if (copyBtn) {
    const icon = copyBtn.querySelector("i");
    copyBtn.addEventListener("click", () => {
      let plainText;
      if (sender === "bot") {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = row.querySelector(".message-text").innerHTML;
        plainText = tempDiv.textContent || tempDiv.innerText || "";
      } else {
        plainText = row.querySelector(".message-text").innerText;
      }
      
      navigator.clipboard.writeText(plainText).then(() => {
        if (icon) {
          icon.classList.remove("fa-copy");
          icon.classList.add("fa-check");
          copyBtn.classList.add("copied");
        }
        setTimeout(() => {
          if (icon) {
            icon.classList.remove("fa-check");
            icon.classList.add("fa-copy");
            copyBtn.classList.remove("copied");
          }
        }, 1500);
      }).catch(err => {
        console.error("Copy failed:", err);
      });
    });
  }
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function showTyping() {
  if (typingIndicator) {
    typingIndicator.style.display = "flex";
    forceScrollToBottom();
  }
}

function hideTyping() {
  if (typingIndicator) {
    typingIndicator.style.display = "none";
    forceScrollToBottom();
  }
}

// Scroll ke bawah saat halaman pertama kali load
setTimeout(() => {
  forceScrollToBottom();
}, 100);

window.addEventListener('resize', () => {
  forceScrollToBottom();
});