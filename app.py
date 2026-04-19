from flask import Flask, render_template, request, jsonify
from model.chatbot import chatbot
import os

os.environ['WEB_MODE'] = 'true'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'reply': 'Halo! Ada yang bisa saya bantu?'})
        
        bot_response = chatbot(user_message)
        return jsonify({'reply': bot_response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reply': 'Maaf, terjadi kesalahan. Silakan coba lagi.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)