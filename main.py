import telebot

BOT_TOKEN = "8371104768:AAE8GYjVBeF0H4fqOur9tMLe4_D4laCBRsk"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "שלום! הבוט שלך מוכן ומחכה לפקודות 😊")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"קיבלת: {message.text}")

print("הבוט מופעל...")
bot.infinity_polling()
