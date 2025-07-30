import telebot
import time
import threading
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(BOT_TOKEN)

def read_products():
    if not os.path.exists("products.txt"):
        return []
    with open("products.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def post_to_channel(product_line):
    parts = product_line.split("\t")
    if len(parts) < 13:
        return
    product_id, image_url, _, description, original_price, sale_price, discount, _, _, _, _, orders, rating, purchase_link = parts

    caption = (
        "🔥 אל תפספסו! מוצר חדש הגיע לערוץ! 🔥\n\n"
        f"🛍️ {description.strip()}\n"
        f"💸 מחיר מבצע: {sale_price.strip()} (מחיר מקורי: {original_price.strip()})\n"
        f"🎯 חיסכון של: {discount.strip()}\n"
        f"⭐️ דירוג: {rating.strip()}%\n"
        f"📦 הזמנות: {orders.strip()}\n\n"
        f"👇🛍הזמינו עכשיו🛍👇\n"
        f"{purchase_link.strip()}\n\n"
        f"מספר פריט: {product_id.strip()}\n\n"
        "להצטרפות לערוץ לחצו עליי👉 https://t.me/+LCv-Xuy6z9RjY2I0"
    )

    try:
        bot.send_photo(CHANNEL_ID, photo=image_url.strip(), caption=caption)
    except Exception as e:
        print(f"Error sending post: {e}")

def schedule_posts():
    products = read_products()
    for i, product in enumerate(products):
        delay = i * 20 * 60  # every 20 minutes
        threading.Timer(delay, post_to_channel, args=[product]).start()

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔️ אין לך הרשאות לבצע פעולה זו.")
        return
    with open("products.txt", "w", encoding="utf-8") as f:
        f.write(message.text)
    bot.send_message(message.chat.id, "✅ הנתונים התקבלו ונשמרו. הפוסטים יתחילו להישלח 🎯")
    schedule_posts()

print("Starting bot...")
schedule_posts()
bot.polling()
