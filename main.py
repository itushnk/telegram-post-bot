import telebot
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(BOT_TOKEN)

def read_next_post():
    if not os.path.exists("posts.txt"):
        return None

    with open("posts.txt", "r", encoding="utf-8") as f:
        posts = f.read().strip().split("
---
")

    if not posts:
        return None

    next_post = posts.pop(0).strip()

    with open("posts.txt", "w", encoding="utf-8") as f:
        f.write("
---
".join(posts))

    return next_post

def send_next_post():
    post_text = read_next_post()
    if post_text:
        bot.send_message(CHANNEL_ID, post_text, parse_mode="HTML", disable_web_page_preview=False)
    else:
        print("אין פוסטים לשליחה כרגע.")

if __name__ == "__main__":
    time.sleep(5)
    send_next_post()
