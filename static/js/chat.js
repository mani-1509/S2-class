const socket = io.connect();

const receiver_id = document.getElementById("receiver_id").value;

socket.emit("join_room", { receiver_id: receiver_id });

// Function to send a message
function sendMessage() {
  const messageContent = document.getElementById("message").value.trim();

  if (messageContent) {
    // Emit the message to the server
    socket.emit("send_message", {
      receiver_id: receiver_id,
      message: messageContent,
    });

    // Append the message immediately to the sender's chat box
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `
      <div>
        <p class="userMsg">${messageContent} <strong class="you">:You</strong></p>
      </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear the input field
    document.getElementById("message").value = "";
  }
}

// Function to append messages to the chat box
function appendMessage(sender, messageContent, cssClass) {
  const chatBox = document.getElementById("chat-box");

  const messageDiv = document.createElement("div");
  messageDiv.innerHTML = `
    <p class="${cssClass}">
      <strong>${sender}:</strong> ${messageContent}
    </p>
  `;
  chatBox.appendChild(messageDiv);

  // Scroll to the bottom of the chat box
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Listen for incoming messages
socket.on("receive_message", function (data) {
  appendMessage(data.sender, data.content, "receiverMsg");
});

// Event listener for pressing Enter to send messages
document.getElementById("message").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});
