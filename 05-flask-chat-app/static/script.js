const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chat-messages");

let cachedLocation = null;

// 1. Ask the browser for GPS coordinates (returns { lat, lon } or null if denied)
function getUserLocation() {
  return new Promise((resolve) => {
    if (cachedLocation) {
      return resolve(cachedLocation);
    }
    if (!navigator.geolocation) {
      return resolve(null);
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        cachedLocation = {
          lat: Number(position.coords.latitude.toFixed(4)),
          lon: Number(position.coords.longitude.toFixed(4)),
        };
        resolve(cachedLocation);
      },
      () => {
        // User clicked "Block" or GPS timed out — continue without location
        resolve(null);
      },
      { timeout: 8000 }
    );
  });
}

// Helper to append message bubbles to the chat window
function addMessage(text, sender) {
  const article = document.createElement("article");
  article.className = `message ${sender}-message`;
  const p = document.createElement("p");
  p.textContent = text;
  article.appendChild(p);
  chatMessages.appendChild(article);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 2. Send message + GPS location to your Flask /api/chat endpoint
chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";

  const location = await getUserLocation();

  try {
    const response = await fetch("http://127.0.0.1:5000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Include X-API-Key here if you enabled token auth in Flask
      },
      body: JSON.stringify({
        message: message,
        location: location,
      }),
    });

    const data = await response.json();
    addMessage(data.response || data.error || "Something went wrong.", "bot");
  } catch (err) {
    addMessage("Could not connect to the Flask server.", "bot");
  }
});
