
import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_PUBLIC_DOMAIN")

if not BOT_TOKEN:
    raise ValueError("❌ שגיאה: טוקן הבוט לא נמצא במשתני סביבה!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    print("📥 עדכון שהתקבל מהטלגרם:", update)

    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        reply = f"👋 קיבלתי את ההודעה שלך: {text}"
        send_message(chat_id, reply)

    return {"ok": True}

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    print("📤 תגובה נשלחה:", response.text)

def set_webhook():
    if not RAILWAY_URL:
        print("⚠️ לא נמצא משתנה RAILWAY_PUBLIC_DOMAIN. לא ניתן להגדיר webhook.")
        return
    webhook_url = f"https://{RAILWAY_URL}/webhook"
    response = requests.get(f"{TELEGRAM_API_URL}/setWebhook", params={"url": webhook_url})
    print("🔗 הגדרת webhook:", response.text)

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=8080)
