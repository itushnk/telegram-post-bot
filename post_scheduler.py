import json
import time

POSTS_FILE = 'posts.json'

def load_posts():
    try:
        with open(POSTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def schedule_next_post(posts):
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print("פוסט הבא יתוזמן בעוד 20 דקות.")
    time.sleep(20 * 60)