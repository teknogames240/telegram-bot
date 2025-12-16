import feedparser
import json
import os
import logging
from datetime import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    JobQueue
)

logging.basicConfig(level=logging.INFO)

CHAT_FILE = "chats.json"

RSS_FEEDS = [
    "https://ai.googleblog.com/feeds/posts/default",
    "https://openai.com/blog/rss.xml",
    "https://venturebeat.com/ai/feed/",
]

# ---------- ابزار ----------
def load_chats():
    if not os.path.exists(CHAT_FILE):
        return []
    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_chat(chat_id):
    chats = load_chats()
    if chat_id not in chats:
        chats.append(chat_id)
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(chats, f)

def get_news():
    messages = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:2]:
            messages.append(f"📰 {entry.title}\n{entry.link}")
    return "\n\n".join(messages)

# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_chat(chat_id)

    await update.message.reply_text(
        "✅ ربات فعال شد!\n"
        "اخبار هوش مصنوعی هر روز ساعت ۹ صبح ارسال می‌شود."
    )

async def send_daily_news(context: ContextTypes.DEFAULT_TYPE):
    news = get_news()
    chats = load_chats()

    for chat_id in chats:
        try:
            await context.bot.send_message(chat_id=chat_id, text=news)
        except Exception as e:
            logging.error(f"Send failed {chat_id}: {e}")

# ---------- Application ----------
def build_application(token: str) -> Application:
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(
        send_daily_news,
        time=time(hour=9, minute=0)
    )

    return app

def set_webhook(token: str, url: str):
    import requests
    hook_url = f"https://api.telegram.org/bot{token}/setWebhook"
    r = requests.post(hook_url, data={"url": url})
    logging.info(f"Webhook set: {r.text}")
