
import telebot
from flask import Flask, request
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ שגיאה: טוקן הבוט לא נמצא במשתני סביבה!")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("📥 התקבל POST מ-Telegram")
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        print("❌ סוג תוכן לא תקין:", request.headers.get('content-type'))
        return 'Invalid content type', 403

@app.route('/')
def index():
    return 'הבוט פעיל ✅'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
