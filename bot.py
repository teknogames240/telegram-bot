import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import parse_qs, urlparse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
from datetime import time
import json

# توکن از Environment Variable
TELEGRAM_BOT_TOKEN = "7256343666:AAGHKZDpAQe3hrAj99hULLJCS-1SZULumMs"

# فایل ذخیره Chat IDها
CHAT_IDS_FILE = "chat_ids.json"

# بارگذاری Chat IDهای قبلی
if os.path.exists(CHAT_IDS_FILE):
    with open(CHAT_IDS_FILE, "r") as f:
        CHAT_IDS = set(json.load(f))
else:
    CHAT_IDS = set()

# تابع ذخیره Chat IDها در فایل
def save_chat_ids():
    with open(CHAT_IDS_FILE, "w") as f:
        json.dump(list(CHAT_IDS), f)

# تابع گرفتن خبرهای AI
def get_ai_news():
    url = "https://www.google.com/search?q=AI+news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news = []
    for a in soup.find_all("a", href=re.compile(r"/url\?q=")):
        if a.h3:
            title = a.h3.text
            href = a["href"]
            parsed_url = urlparse(href)
            actual_link = parse_qs(parsed_url.query).get("q", [None])[0]
            if actual_link:
                news.append(f"{title}\n{actual_link}\n")
    return news

# ارسال خبر به تمام کاربران
async def send_news(context: ContextTypes.DEFAULT_TYPE):
    news = get_ai_news()
    message = "AI News Update:\n\n" + "\n".join(news[:5]) if news else "No AI news found."
    
    for chat_id in CHAT_IDS:
        await context.bot.send_message(chat_id=chat_id, text=message)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in CHAT_IDS:
        CHAT_IDS.add(chat_id)
        save_chat_ids()  # ذخیره در فایل
    await update.message.reply_text(
        "Welcome to the AI News Bot! I will send you AI news updates daily."
    )

# اجرای ربات
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # اضافه کردن فرمان /start
    app.add_handler(CommandHandler("start", start))

    # JobQueue برای ارسال خبر روزانه ساعت 9 صبح
    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(send_news, time=time(hour=9, minute=0))

    # اجرای polling
    app.run_polling()

if __name__ == "__main__":
    main()
