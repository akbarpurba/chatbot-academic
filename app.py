from flask import Flask, render_template, request, jsonify
from model.chatbot import chatbot

app = Flask(__name__)

# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# CHAT ENDPOINT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.json["message"]
        reply = chatbot(msg)
        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)  # tampil di terminal
        return jsonify({"reply": "Server error: " + str(e)})

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)