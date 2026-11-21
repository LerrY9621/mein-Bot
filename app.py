from flask import Flask, request
import os, requests

app = Flask(__name__)

ID = os.environ.get("GREEN_ID")
TOKEN = os.environ.get("GREEN_TOKEN")
GROQ_KEY = os.environ.get("GROQ_API_KEY")

def ask_ai(text):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Du bist ein hilfreicher Bot, antwortest auf Deutsch, kurz und direkt."},
                {"role": "user", "content": text}
            ]
        },
        timeout=30
    )
    return r.json()["choices"][0]["message"]["content"]

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    data = request.json
    try:
        msg = data.get("bodyData", {}).get("messageData", {})
        if msg.get("typeMessage") == "textMessage":
            text = msg["textMessageData"]["textMessage"]
            sender = data["bodyData"]["senderData"]["chatId"]
            answer = ask_ai(text)
            requests.post(
                f"https://api.green-api.com/waInstance{ID}/sendMessage/{TOKEN}",
                json={"chatId": sender, "message": answer}
            )
    except Exception as e:
        print(e)
    return "OK"

@app.route("/")
def home():
    return "Bot laeuft!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
