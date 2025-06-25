function appendMessage(msg, fromBot = false) {
  const msgBox = document.getElementById("messages");
  const html = `<div class="${fromBot ? 'text-left' : 'text-right'}">
    <p class="inline-block ${fromBot ? 'bg-green-200 text-green-900' : 'bg-blue-200 text-blue-900'} p-3 rounded-xl">${msg}</p>
  </div>`;
  msgBox.innerHTML += html;
  msgBox.scrollTop = msgBox.scrollHeight;

  // Speak reply if it's from bot
  if (fromBot) {
    speak(msg);
  }
}

function sendMessage() {
  const userInput = document.getElementById("user_input");
  const msg = userInput.value.trim();
  if (!msg) return;

  appendMessage(msg, false);

  const msgBox = document.getElementById("messages");
  const typingDiv = document.createElement("div");
  typingDiv.id = "typing";
  typingDiv.className = "text-left";
  typingDiv.innerHTML = `<p class="inline-block bg-gray-200 text-gray-800 p-3 rounded-xl italic animate-pulse">Typing...</p>`;
  msgBox.appendChild(typingDiv);
  msgBox.scrollTop = msgBox.scrollHeight;

  fetch("/get", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("typing").remove();
      appendMessage(data.reply, true);
    });

  userInput.value = "";
  userInput.focus();
}

document.addEventListener("DOMContentLoaded", () => {
  appendMessage(" Hello! I'm your VSB College Assistant. Ask me anything about courses, hostel, fees, or admission!", true);

  const input = document.getElementById("user_input");
  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });
});

function speak(text) {
  if (!'speechSynthesis' in window) return;

  const processed = text.replace(/\b\d{6,}\b/g, match => match.split("").join(" "));

  const synth = window.speechSynthesis;
  const utter = new SpeechSynthesisUtterance(processed);

  const voices = synth.getVoices();
  const englishVoices = voices.filter(v => v.lang.startsWith("en") && v.name.toLowerCase().includes("female"));

  utter.voice = englishVoices.length > 0 ? englishVoices[0] : voices[0];
  utter.pitch = 1;
  utter.rate = 1;
  utter.volume = 1;
  utter.lang = "en-US";

  synth.cancel();
  synth.speak(utter);
}
