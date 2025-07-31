import telebot
from flask import Flask, request
import os

# קבלת הטוקן ממשתני הסביבה
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN or ' ' in BOT_TOKEN:
    raise ValueError("❌ שגיאה: טוקן הבוט לא מוגדר או מכיל רווחים!")

# יצירת מופע של הבוט
bot = telebot.TeleBot(BOT_TOKEN)

# הגדרת ה-Flask app
app = Flask(__name__)

# קביעת הנתיב ל-webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

# דף בית לבדיקה פשוטה
@app.route('/')
def index():
    return '✅ הבוט פעיל ומחכה לעדכונים מ-Telegram!'

# הרצת השרת
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
