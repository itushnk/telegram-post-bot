
import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RAILWAY_STATIC_URL')}/webhook"

# Set the webhook automatically when the server starts
def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    print("Set webhook response:", response.text)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received update:", data)

    if "message" in data and "chat" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = "תודה! הבוט מחובר ועובד ✅"

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text}
        )

    return {"ok": True}

@app.route('/')
def index():
    return 'הבוט פעיל וממתין לעדכונים'

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=8080)
