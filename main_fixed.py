
import os
import telebot
from flask import Flask, request

# קבלת הטוקן מהסביבה
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN or " " in BOT_TOKEN:
    raise ValueError("טוקן הבוט לא תקין או מכיל רווחים")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# מסלול ההוק
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    else:
        return "Invalid content type", 403

# בדיקה בסיסית שהבוט עונה
@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "שלום! הבוט פעיל ומוכן לשירותך 🤖")

# הפעלת השרת
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
