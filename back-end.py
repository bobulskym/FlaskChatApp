from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

chat_history = []

@app.route('/chat', methods=['GET'])
def get_chat():
    return jsonify({'chat': chat_history})

@app.route('/chat', methods=['POST'])
def post_chat():
    data = request.json
    nickname = data.get('nickname')
    message = data.get('message')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not nickname or not message:
        return jsonify({'error': 'Nickname and message are required!'}), 400
    
    chat_entry = {'nickname': nickname, 'message': message, 'timestamp': timestamp}
    chat_history.append(chat_entry)
    
    return jsonify({'success': True, 'chat': chat_entry})

@app.route('/chat/clear', methods=['POST'])
def clear_chat():
    global chat_history
    chat_history = []
    return jsonify({'success': True, 'message': 'Chat history cleared'})

if __name__ == '__main__':
    app.run(debug=True)
