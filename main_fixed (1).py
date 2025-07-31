
import os
import telebot
import time
import schedule
from flask import Flask, request

# קבלת הטוקן וה-CHAT_ID ממשתני סביבה
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # לדוגמה: "@MyChannelName"

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("Missing BOT_TOKEN or CHANNEL_ID environment variable")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# טעינת הפוסטים מקובץ טקסט
POSTS_FILE = "posts.txt"
sent_index = 0

def load_posts():
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        raw = f.read().split("=====")
        return [p.strip() for p in raw if p.strip()]

posts = load_posts()

def send_post():
    global sent_index
    if sent_index >= len(posts):
        print("✅ All posts sent.")
        return
    post = posts[sent_index]
    try:
        # ניתוח טקסט + תמונה
        if "IMAGE_URL:" in post:
            parts = post.split("IMAGE_URL:")
            caption = parts[0].strip()
            image_url = parts[1].strip()
            bot.send_photo(CHANNEL_ID, photo=image_url, caption=caption, parse_mode="HTML")
        else:
            bot.send_message(CHANNEL_ID, post, parse_mode="HTML")
        print(f"✅ Post {sent_index + 1} sent.")
        sent_index += 1
    except Exception as e:
        print(f"❌ Failed to send post: {e}")

# הגדרת המשימה החוזרת כל 20 דקות
schedule.every(20).minutes.do(send_post)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Unsupported Media Type', 415

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
