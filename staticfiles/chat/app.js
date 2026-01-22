const API_URL = "/api/tanya/";
const chatBox = document.getElementById("chatBox");
const input = document.getElementById("questionInput");

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerHTML = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

async function sendQuestion() {
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";

  const botMsg = addMessage("⏳ Sedang memproses...", "bot");

  let seconds = 0;
  const timer = setInterval(() => {
    seconds++;
    botMsg.innerHTML = `⏳ Sedang memproses... (${seconds} detik)`;
  }, 1000);

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pertanyaan: question })
    });

    const data = await res.json();
    clearInterval(timer);

    botMsg.innerHTML = data.jawaban || "Tidak ditemukan jawaban yang relevan.";
  } catch (e) {
    clearInterval(timer);
    botMsg.innerHTML = "❌ Gagal menghubungi server.";
  }
}
