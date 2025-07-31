import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

WEBHOOK_PATH = f"/{API_TOKEN}"
WEBHOOK_URL = f"https://your-app-name.up.railway.app{WEBHOOK_PATH}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "הבוט מופעל בהצלחה!")

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
