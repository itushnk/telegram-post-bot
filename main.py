import telebot
import os
import time

BOT_TOKEN = "8371104768:AAE8GYjVBeF0H4fqOur9tMLe4_D4laCBRsk"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "הבוט פעיל!")

print("הבוט מופעל...")
bot.infinity_polling()
