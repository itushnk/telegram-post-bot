import os
import time
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # דוגמה: "@YourChannelName"

bot = telebot.TeleBot(TOKEN)

def get_next_post():
    try:
        with open("posts.txt", "r", encoding="utf-8") as file:
            posts = file.readlines()
        if not posts:
            return None
        next_post = posts[0].strip()
        # Remove the first post after sending
        with open("posts.txt", "w", encoding="utf-8") as file:
            file.writelines(posts[1:])
        return next_post
    except Exception as e:
        print("Error reading posts:", e)
        return None

while True:
    post = get_next_post()
    if post:
        try:
            bot.send_message(CHANNEL_ID, post, parse_mode="HTML")
            print("Post sent!")
        except Exception as e:
            print("Error sending post:", e)
    else:
        print("No posts to send.")
    time.sleep(1200)  # כל 20 דקות (20*60 = 1200 שניות)