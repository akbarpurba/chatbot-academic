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
  if (icon) {
    if (isDark) {
      icon.classList.remove('fa-moon');
      icon.classList.add('fa-sun');
    } else {
      icon.classList.remove('fa-sun');
      icon.classList.add('fa-moon');
    }
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

// ==================== CHAT FUNCTIONS ====================
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

document.querySelectorAll(".chip").forEach((btn) => {
  btn.addEventListener("click", () => {
    input.value = btn.dataset.query;
    sendMessage();
  });
});

// ==================== FUNGSI FORMAT PESAN (DENGAN DUKUNGAN **BOLD**) ====================
function formatBotMessage(text) {
  // JANGAN escape HTML terlebih dahulu - biarkan tag HTML tetap utuh
  let formatted = text;
  
  // =========================
  // FORMAT DOUBLE BINTANG (**teks**) MENJADI <strong>teks</strong>
  // =========================
  // Pola: **teks** (non-greedy, tidak termasuk tag HTML di dalamnya)
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // Ubah newline menjadi <br>
  formatted = formatted.replace(/\n/g, '<br>');
  
  // Format bullet points (•) - hanya jika bukan bagian dari tag HTML
  formatted = formatted.replace(/(?![^<]*>)(•)/g, '<span class="bullet-point">•</span>');
  
  // Format nomor (1., 2., 3., dll) - hanya jika bukan bagian dari tag HTML
  formatted = formatted.replace(/(?![^<]*>)(\d+)\./g, '<span class="number-point">$1.</span>');
  
  // Format teks tebal untuk judul (teks diikuti titik dua) - HINDARI DOUBLE BINTANG YANG SUDAH DIPROSES
  // Gunakan negative lookbehind untuk menghindari teks yang sudah dalam tag <strong>
  formatted = formatted.replace(/^([^<strong>][^<br>]*?):/gm, '<strong>$1:</strong>');
  formatted = formatted.replace(/\n([^<strong>][^<br>]*?):/g, '\n<strong>$1:</strong>');
  
  return formatted;
}

// ==================== DECODE HTML UNTUK KOPI ====================
function decodeHTML(html) {
  const txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}

// ==================== SEND MESSAGE ====================
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

    // Decode HTML untuk mendapatkan teks asli
    const decodedReply = decodeHTML(data.reply);
    // Format pesan tanpa escape HTML
    const formattedReply = formatBotMessage(decodedReply);
    addMessage(formattedReply, "bot");
  } catch (err) {
    console.error("Error:", err);
    hideTyping();
    addMessage("Maaf, terjadi kesalahan. Silakan coba lagi.", "bot");
  }
}

// ==================== ADD MESSAGE TO CHAT ====================
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
    // Untuk user message, escape HTML untuk keamanan
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
  messagesArea.scrollTop = messagesArea.scrollHeight;

  // Add copy button functionality
  const copyBtn = row.querySelector(".copy-msg-btn");
  if (copyBtn) {
    const icon = copyBtn.querySelector("i");
    copyBtn.addEventListener("click", () => {
      // Ambil teks asli (untuk bot, ambil innerText yang sudah di-decode)
      let plainText;
      if (sender === "bot") {
        // Buat elemen temporary untuk decode HTML
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

// ==================== ESCAPE HTML UNTUK KEAMANAN ====================
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ==================== TYPING INDICATOR ====================
function showTyping() {
  if (typingIndicator) {
    typingIndicator.style.display = "flex";
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }
}

function hideTyping() {
  if (typingIndicator) {
    typingIndicator.style.display = "none";
  }
}