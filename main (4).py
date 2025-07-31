
import os
import requests
from flask import Flask, request

app = Flask(__name__)

# === CONFIGURATION ===
BOT_TOKEN = "8371104768:AAE8GYjVBeF0H4fqOur9tMLe4_D4laCBRsk"
BOT_USERNAME = "MyPostBot2025_bot"
WEBHOOK_URL = "https://telegram-post-bot-production.up.railway.app/webhook"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# === SET WEBHOOK ===
def set_webhook():
    response = requests.post(f"{TELEGRAM_API_URL}/setWebhook", data={"url": WEBHOOK_URL})
    print("Webhook Setup Response:", response.json())
    return response.json()

# === MAIN ROUTE FOR WEBHOOK ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming update:", data)

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        reply_text = "תודה על ההודעה שלך! 🤖 הבוט עובד."

        # Respond back
        send_message(chat_id, reply_text)

    return {'ok': True}

# === FUNCTION TO SEND MESSAGE ===
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    print("Send Message Response:", response.json())
    return response.json()

# === SET WEBHOOK ON STARTUP ===
if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=8080)
