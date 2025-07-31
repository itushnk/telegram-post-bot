import telebot
import os
import time

# טוקן מהסביבה
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("❌ שגיאה: טוקן הבוט לא נמצא במשתני סביבה!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "היי! הבוט פועל בהצלחה 🎉")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def run_bot():
    print("הבוט מופעל...")
    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=20)
        except telebot.apihelper.ApiTelegramException as e:
            if "409" in str(e):
                print("⚠️ שגיאה: הבוט כבר פעיל במקום אחר. ודא שאין מופעים כפולים.")
            else:
                print(f"שגיאה אחרת: {e}")
            time.sleep(10)
        except Exception as e:
            print(f"שגיאה כללית: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
