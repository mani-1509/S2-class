function sendMessage() {
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  if (userInput.value.trim() !== "") {
    // Display user message
    const userMessage = `<div class="message user-message"><b>You:</b> ${userInput.value}</div>`;
    chatBox.innerHTML += userMessage;

    // Send POST request to server
    fetch("/get_response", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput.value }),
    })
      .then((response) => response.json())
      .then((data) => {
        const botMessage = `<div class="message bot-message"><b>ChatBot:</b> ${data.response}</div>`;
        chatBox.innerHTML += botMessage;

        // Auto-scroll chatbox
        chatBox.scrollTop = chatBox.scrollHeight;
      });

    userInput.value = "";
  }
}
