import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import parse_qs, urlparse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
from datetime import time

# Token و Chat ID از Environment Variable
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID"))

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

# ارسال خبر
async def send_news(context: ContextTypes.DEFAULT_TYPE):
    news = get_ai_news()
    if news:
        message = "AI News Update:\n\n" + "\n".join(news[:5])
        await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    else:
        await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="No AI news found.")

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the AI News Bot! I will send you AI news updates daily.")

# اجرای ربات
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # JobQueue برای ارسال خبر روزانه ساعت 9 صبح
    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(send_news, time=time(hour=9, minute=0))

    app.run_polling()

if __name__ == "__main__":
    main()
