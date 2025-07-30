
import os
import time
import telebot
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(TOKEN)

POSTS_FILE = "posts.txt"
TEMP_IMAGE = "temp_image.jpg"

def download_image(url, filename):
    try:
        r = requests.get(url, stream=True, timeout=15)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return True
        else:
            print(f"Failed to download image. Status code: {r.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

def get_next_post():
    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
        if not lines:
            return None, None
        line = lines[0].strip()
        with open(POSTS_FILE, "w", encoding="utf-8") as file:
            file.writelines(lines[1:])
        if '|' in line:
            text, img_url = line.split('|', 1)
        else:
            text, img_url = line, None
        return text.strip(), img_url.strip() if img_url else None
    except Exception as e:
        print(f"Error reading posts: {e}")
        return None, None

def main():
    while True:
        post_text, image_url = get_next_post()
        if post_text:
            post_text = post_text.replace('\n', '\n')
            try:
                if image_url:
                    if download_image(image_url, TEMP_IMAGE):
                        with open(TEMP_IMAGE, 'rb') as photo:
                            bot.send_photo(CHANNEL_ID, photo)
                        os.remove(TEMP_IMAGE)
                    else:
                        print("שליחה ללא תמונה כי ההורדה נכשלה")
                bot.send_message(CHANNEL_ID, post_text, parse_mode="HTML")
                print("פוסט נשלח בהצלחה!")
            except Exception as e:
                print(f"שגיאה בשליחת הפוסט: {e}")
        else:
            print("אין פוסטים לשליחה כרגע.")
            time.sleep(300)
            continue
        time.sleep(20*60)

if __name__ == "__main__":
    main()
    