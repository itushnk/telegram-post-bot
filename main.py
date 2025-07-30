import time
import csv
import requests
import schedule
import telegram
from telegram import InputMediaPhoto
from datetime import datetime
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
bot = telegram.Bot(token=TOKEN)

def read_posts():
    with open("products.csv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        posts = []
        for row in reader:
            if len(row) >= 13:
                product_id, img_url, _, title, original_price, sale_price, _, _, _, _, _, rating, link = row[:13]
                try:
                    response = requests.get(img_url)
                    image_bytes = response.content
                    discount = round((float(original_price[4:]) - float(sale_price[4:])) / float(original_price[4:]) * 100)
                    post_text = f"פוסט חדש בערוץ!\n\n📌 {title}\n💰 מחיר מבצע: {sale_price}\n🧾 מחיר רגיל: {original_price}\n💸 חיסכון: {discount}%\n⭐ דירוג: {rating}\n\n👇🛍הזמינו עכשיו🛍👇\n{link}\n\n🆔 מספר פריט: {product_id}\nכל המחירים והמבצעים תקפים למועד הפרסום ועשויים להשתנות."
                    posts.append((post_text, image_bytes))
                except Exception as e:
                    print("Error processing row:", e)
        return posts

def post_to_telegram():
    global post_index
    if post_index < len(posts):
        text, image = posts[post_index]
        bot.send_photo(chat_id=CHANNEL_ID, photo=image, caption=text)
        print(f"Post sent: {datetime.now()}")
        post_index += 1
    else:
        print("No more posts to send.")

posts = read_posts()
post_index = 0
schedule.every(20).minutes.do(post_to_telegram)

print("Bot started. Waiting to send posts...")
while True:
    schedule.run_pending()
    time.sleep(1)