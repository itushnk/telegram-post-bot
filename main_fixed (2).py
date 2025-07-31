
import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_URL = os.getenv("RAILWAY_PUBLIC_DOMAIN")  # Without https://

if not BOT_TOKEN or not PUBLIC_URL:
    raise Exception("Missing BOT_TOKEN or RAILWAY_PUBLIC_DOMAIN environment variables")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Echo message (for test)
        reply = {"chat_id": chat_id, "text": f"👋 קיבלתי: {text}"}
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=reply)

    return {"status": "ok"}, 200


def set_webhook():
    url = f"https://{PUBLIC_URL}/webhook"
    res = requests.get(f"{TELEGRAM_API_URL}/setWebhook?url={url}")
    print("Webhook setup:", res.json())


if __name__ == "__main__":
    set_webhook()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
