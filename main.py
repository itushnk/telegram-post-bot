import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 📥 מסלול webhook – מקבל את כל העדכונים מטלגרם
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

# 💬 הודעה פשוטה – לדוגמה: תגובה ל"שלום"
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "היי! אני הבוט שלך – מה נשמע? 🤖")

# 🚀 הרצת האפליקציה ב-Railway
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
