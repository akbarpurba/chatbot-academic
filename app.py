from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from model.chatbot import chatbot
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_input = data.get("message")

    reply = chatbot(user_input)

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))