const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messagesArea = document.getElementById("messagesArea");
const typingIndicator = document.getElementById("typingIndicator");

// enable tombol
input.addEventListener("input", () => {
    sendBtn.disabled = input.value.trim() === "";
});

// enter kirim
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});

sendBtn.addEventListener("click", sendMessage);

// quick replies
document.querySelectorAll(".chip").forEach(btn => {
    btn.addEventListener("click", () => {
        input.value = btn.dataset.query;
        sendMessage();
    });
});

// fungsi kirim
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
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await res.json();

        hideTyping();
        addMessage(data.reply, "bot");

    } catch (err) {
        hideTyping();
        addMessage("Server error 😢", "bot");
    }
}

// tampilkan pesan
function addMessage(text, sender) {
    const row = document.createElement("div");
    row.className = `message-row ${sender}-message`;

    row.innerHTML = `
        ${sender === "bot" ? `
        <div class="bot-avatar-mini">
            <div class="avatar-sm">🤖</div>
        </div>` : ``}

        <div class="message-bubble">${text}</div>
    `;

    messagesArea.appendChild(row);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// typing
function showTyping() {
    typingIndicator.style.display = "flex";
}

function hideTyping() {
    typingIndicator.style.display = "none";
}