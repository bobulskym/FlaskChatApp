import eventlet
eventlet.monkey_patch()  # Ensure compatibility

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send
from datetime import datetime, timedelta
import csv
import jwt
import hashlib

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

CHAT_FILE = "chat_history.csv"
USERS_FILE = "users.csv"
SECRET_KEY = "tancovalarybasrakom"

def initialize_files():
    try:
        with open(CHAT_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["nickname", "message", "timestamp"])
    except FileExistsError:
        pass
    
    try:
        with open(USERS_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["nickname", "password_hash"])
    except FileExistsError:
        pass

initialize_files()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(nickname, password):
    users = load_users()
    if nickname in users:
        return False
    with open(USERS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([nickname, hash_password(password)])
    return True

def authenticate_user(nickname, password):
    users = load_users()
    if nickname in users and users[nickname] == hash_password(password):
        return True
    return False

def load_users():
    users = {}
    try:
        with open(USERS_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["nickname"]] = row["password_hash"]
    except FileNotFoundError:
        pass
    return users

def generate_token(nickname):
    payload = {"nickname": nickname, "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["nickname"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def load_chat_history():
    chat_history = []
    try:
        with open(CHAT_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                chat_history.append(row)
    except FileNotFoundError:
        pass
    return chat_history

def save_chat_entry(nickname, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(CHAT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([nickname, message, timestamp])
    return {"nickname": nickname, "message": message, "timestamp": timestamp}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nickname = data.get('nickname')
    password = data.get('password')
    
    if not nickname or not password:
        return jsonify({'error': 'Nickname and password are required!'}), 400
    
    if register_user(nickname, password):
        return jsonify({'success': True})
    return jsonify({'error': 'Nickname already taken!'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    nickname = data.get('nickname')
    password = data.get('password')
    
    if authenticate_user(nickname, password):
        token = generate_token(nickname)
        return jsonify({'success': True, 'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/chat', methods=['GET'])
def get_chat():
    token = request.headers.get("Authorization")
    user = verify_token(token)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'chat': load_chat_history()})

@app.route('/chat/clear', methods=['POST'])
def clear_chat():
    token = request.headers.get("Authorization")
    user = verify_token(token)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    with open(CHAT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["nickname", "message", "timestamp"])
    return jsonify({'success': True, 'message': 'Chat history cleared'})

@socketio.on("message")
def handle_message(data):
    token = data.get("token")
    user = verify_token(token)
    if not user:
        return

    message = data.get("message")
    chat_entry = save_chat_entry(user, message)
    
    # Broadcast the message to all connected clients
    send(chat_entry, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

