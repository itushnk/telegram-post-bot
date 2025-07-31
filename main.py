from flask import Flask, request
import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ שגיאה: טוקן הבוט לא נמצא במשתני סביבה!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "הבוט מופעל!"

@app.route('/send', methods=['POST'])
def send_post():
    data = request.get_json()
    if not data or 'chat_id' not in data or 'text' not in data:
        return "❌ נתונים חסרים", 400
    try:
        bot.send_message(data['chat_id'], data['text'], parse_mode='HTML')
        return "✅ ההודעה נשלחה", 200
    except Exception as e:
        return f"שגיאה בשליחה: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)