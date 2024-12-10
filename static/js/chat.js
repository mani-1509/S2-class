const socket = io.connect();
const receiver_id = document.getElementById("receiver_id").value;

// Join the chat room
socket.emit("join_room", { receiver_id: receiver_id });

// Send a message
function sendMessage() {
  const messageContent = document.getElementById("message").value;

  if (messageContent.trim() !== "") {
    socket.emit("send_message", {
      receiver_id: receiver_id,
      message: messageContent,
    });

    // Add the sent message immediately to the chat box for the sender
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

// Receive a message
socket.on("receive_message", function (data) {
  const chatBox = document.getElementById("chat-box");

  // Display the received message in the chat box
  chatBox.innerHTML += `
    <div>
      <p class="receiverMsg">
        <strong class="receiver">${data.sender}:</strong> ${data.content}
      </p>
    </div>
  `;
  chatBox.scrollTop = chatBox.scrollHeight;
});
