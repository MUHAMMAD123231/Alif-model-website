// static/interaction/chat.js
// Socket.IO chat client for all discussion pages

const socket = io();

// Get room name from URL or page context
const room = document.body.getAttribute('data-room') || 'general';
const username = document.body.getAttribute('data-username') || 'Guest';
const role = document.body.getAttribute('data-role') || 'guest';

// Join room
socket.emit('join', { room, username });

// Handle incoming messages
socket.on('receive_message', data => {
  addMessage(data.username, data.message);
});

// Handle status updates (join/leave)
socket.on('status', data => {
  addStatus(data.msg);
});

// Send message
function sendMessage() {
  const input = document.getElementById('chat-input');
  const message = input.value.trim();
  if (message) {
    socket.emit('send_message', { room, username, message });
    input.value = '';
  }
}

// Add message to chat UI
function addMessage(user, msg) {
  const chatBox = document.getElementById('chat-box');
  const div = document.createElement('div');
  let avatar = '';
  let styleClass = '';
  let time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  // Use username from DB (already passed as 'user')
  if (user === username) {
    styleClass = 'tg-chat-message user';
    avatar = '🧑';
  } else if (user.toLowerCase().includes('admin')) {
    styleClass = 'tg-chat-message other';
    avatar = '🛡️';
  } else if (role === 'teacher' || user.toLowerCase().includes('teacher')) {
    styleClass = 'tg-chat-message other';
    avatar = '👩‍🏫';
  } else {
    styleClass = 'tg-chat-message other';
    avatar = '👤';
  }
  div.className = styleClass;
  div.innerHTML = `
    <span class="tg-chat-avatar">${avatar}</span>
    <span class="tg-chat-username">${user}</span>
    <span class="tg-chat-text">${msg}</span>
    <small>${time}</small>
  `;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Add status to chat UI
function addStatus(msg) {
  const chatBox = document.getElementById('chat-box');
  const div = document.createElement('div');
  div.className = 'chat-status';
  div.innerText = msg;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Event listener for send button
const sendBtn = document.getElementById('chat-send');
const input = document.getElementById('chat-input');
if (sendBtn && input) {
  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendMessage();
  });
  input.addEventListener('input', () => {
    sendBtn.disabled = input.value.trim().length === 0;
  });
  // Initial state
  sendBtn.disabled = true;
}
