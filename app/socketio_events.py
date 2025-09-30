# SocketIO event handlers for chat
# - Handles join, leave, send_message, and other real-time events
# - Used for real-time chat in classroom discussion

from . import socketio
from flask_socketio import emit, join_room, leave_room

@socketio.on('join')
def handle_join(data):
	room = data.get('room')
	username = data.get('username')
	join_room(room)
	emit('status', {'msg': f'{username} has joined the chat.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
	room = data.get('room')
	username = data.get('username')
	leave_room(room)
	emit('status', {'msg': f'{username} has left the chat.'}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
	room = data.get('room')
	username = data.get('username')
	message = data.get('message')
	emit('receive_message', {'username': username, 'message': message}, room=room)
# SocketIO event handlers for chat
# - Handles join, leave, send_message, and other real-time events
# - Used for real-time chat in classroom discussion

# Add your SocketIO event handlers here
