import time
import telebot
from post_formatter import format_post
from post_scheduler import load_posts, schedule_next_post

BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHANNEL_USERNAME = 'YOUR_CHANNEL_USERNAME_HERE'

bot = telebot.TeleBot(BOT_TOKEN)

def send_post():
    posts = load_posts()
    if not posts:
        print("אין פוסטים לשליחה כרגע.")
        return
    post = posts.pop(0)
    formatted_post = format_post(post)
    try:
        bot.send_message(CHANNEL_USERNAME, formatted_post, parse_mode="HTML", disable_web_page_preview=False)
        print("פוסט נשלח בהצלחה!")
    except Exception as e:
        print(f"שגיאה בשליחת הפוסט: {e}")
    schedule_next_post(posts)

if __name__ == "__main__":
    send_post()