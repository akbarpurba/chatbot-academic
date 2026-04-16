const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messagesArea = document.getElementById("messagesArea");
const typingIndicator = document.getElementById("typingIndicator");

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
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();

    hideTyping();

    const decodedReply = decodeHTML(data.reply);

    addMessage(decodedReply, "bot");
  } catch (err) {
    hideTyping();
    addMessage("Server error", "bot");
  }
}
function addMessage(text, sender) {
  const row = document.createElement("div");
  row.className = `message-row ${sender}-message`;

  row.innerHTML = `
        ${
          sender === "bot"
            ? `
        <div class="bot-avatar-mini">
            <div class="avatar-sm">🤖</div>
        </div>`
            : ``
        }

        <div class="message-bubble">
            <span class="message-text">${text}</span>

            <button class="copy-msg-btn" title="Copy">
                <i class="fa-regular fa-copy"></i>
            </button>
        </div>
    `;

  messagesArea.appendChild(row);
  messagesArea.scrollTop = messagesArea.scrollHeight;

  const copyBtn = row.querySelector(".copy-msg-btn");
  const icon = copyBtn.querySelector("i");

  copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(text).then(() => {
      icon.classList.remove("fa-copy");
      icon.classList.add("fa-solid", "fa-check");
      copyBtn.classList.add("copied");

      setTimeout(() => {
        icon.classList.remove("fa-check");
        icon.classList.add("fa-regular", "fa-copy");
        copyBtn.classList.remove("copied");
      }, 1200);
    });
  });
}

function showTyping() {
  typingIndicator.style.display = "flex";
}

function hideTyping() {
  typingIndicator.style.display = "none";
}
