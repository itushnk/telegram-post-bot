
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ שגיאה: טוקן הבוט לא נמצא במשתני סביבה!")

WEBHOOK_URL = "https://telegram-post-bot-production.up.railway.app/webhook"
r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")
print("Webhook response:", r.text)
