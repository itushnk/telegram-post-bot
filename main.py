import telebot
import os

BOT_TOKEN = "8371104768:AAE8GYjVBeF0H4fqOur9tMLe4_D4laCBRsk"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "הבוט מוכן ומחכה לפקודות!")

bot.polling()
