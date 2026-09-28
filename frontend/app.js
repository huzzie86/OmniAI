const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("message");
const mode = document.getElementById("mode");
const status = document.getElementById("status");
const newChat = document.getElementById("newChat");

let history = [];

function addMessage(role, text, meta="") {
  const row = document.createElement("div");
  row.className = `message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  row.appendChild(bubble);
  if (meta) {
    const m = document.createElement("div");
    m.className = "meta";
    m.textContent = meta;
    bubble.appendChild(m);
  }
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

async function checkHealth() {
  try {
    const r = await fetch("/api/health");
    const data = await r.json();
    status.textContent = `● ${data.providers.join(", ")} online`;
  } catch {
    status.textContent = "● offline";
  }
}

async function sendMessage(text) {
  addMessage("user", text);
  history.push({role:"user", content:text});

  const thinking = document.createElement("div");
  thinking.className = "message assistant";
  thinking.innerHTML = '<div class="bubble">Thinking…</div>';
  chat.appendChild(thinking);
  chat.scrollTop = chat.scrollHeight;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message:text, history:history.slice(-12), mode:mode.value})
    });
    const data = await response.json();
    thinking.remove();
    if (!response.ok) throw new Error(data.detail || "Request failed");
    addMessage("assistant", data.answer, `route: ${data.route}`);
    history.push({role:"assistant", content:data.answer});
  } catch (err) {
    thinking.remove();
    addMessage("assistant", `Error: ${err.message}`);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  await sendMessage(text);
});

document.querySelectorAll(".prompt").forEach(btn => {
  btn.addEventListener("click", () => {
    input.value = btn.textContent;
    input.focus();
  });
});

newChat.addEventListener("click", () => {
  history = [];
  chat.innerHTML = "";
  location.reload();
});

input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.requestSubmit();
  }
});

CheckHealth();
