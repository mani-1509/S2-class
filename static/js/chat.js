const socket = io.connect();
const receiver_id = document.getElementById("receiver_id").value;

socket.emit("join_room", { receiver_id: receiver_id });

function sendMessage() {
  const messageContent = document.getElementById("message").value;
  socket.emit("send_message", {
    receiver_id: receiver_id,
    message: messageContent,
  });
  document.getElementById("message").value = "";
}

socket.on("receive_message", function (data) {
  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div><strong>${data.sender}:</strong> ${data.content}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
});
