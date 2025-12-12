import os
import reqimport os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
from datetime import time, timezone, timedelta

# توکن ربات
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# ذخیره‌ی Chat ID کاربران در یک لیست ساده
subscribed_users = set()

# گرفتن اخبار AI از گوگل نیوز
def get_ai_news():
    url = "https://news.google.com/search?q=AI&hl=en-US&gl=US&ceid=US:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    news = []
    for a in soup.find_all("a", href=True):
        title = a.text.strip()
        href = a['href']
        if title and href.startswith("./articles/"):
            link = "https://news.google.com" + href[1:]
            news.append(f"{title}\n{link}\n")
    return news

# ارسال خبر به همه کاربران
async def send_news(context: ContextTypes.DEFAULT_TYPE):
    news = get_ai_news()
    if not news:
        news = ["No AI news found."]
    
    message = "AI News Update:\n\n" + "\n".join(news[:5])
    
    for chat_id in subscribed_users:
        await context.bot.send_message(chat_id=chat_id, text=message)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in subscribed_users:
        subscribed_users.add(chat_id)
    await update.message.reply_text(
        "Welcome to the AI News Bot! You will receive AI news updates daily."
    )

# اجرای ربات
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    job_queue: JobQueue = app.job_queue
    # ارسال روزانه ساعت 9 صبح به وقت ایران
    iran_time = timezone(timedelta(hours=3, minutes=30))
    job_queue.run_daily(send_news, time=time(hour=9, minute=0, tzinfo=iran_time))

    app.run_polling()

if __name__ == "__main__":
    main()
