import feedparser
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from datetime import time

logging.basicConfig(level=logging.INFO)

# خواندن توکن از محیط (دیگر هاردکد نیست)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# این چک کردن دیگر لازم نیست چون در app.py انجام می‌شود، اما برای اطمینان نگه می‌داریم
if not TELEGRAM_BOT_TOKEN:
    print("FATAL: TELEGRAM_BOT_TOKEN environment variable not set.")
    exit()

RSS_SOURCES = [
    "https://ai.googleblog.com/feeds/posts/default",
    "https://openai.com/blog/rss.xml",
    "https://venturebeat.com/ai/feed/",
    "https://digiato.com/feed",
]

# توابع باید async باشند
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """جواب دادن به فرمان /start"""
    message = "به ربات خبر هوش مصنوعی خوش آمدید! با من می‌توانید جدیدترین اخبار را دریافت کنید."
    await update.message.reply_text(message) # استفاده از await ضروری است

# توابع باید async باشند
async def send_news(context: ContextTypes.DEFAULT_TYPE):
    """ارسال اخبار روزانه به چت‌ها (نیاز به منطق کامل)"""
    # در اینجا باید منطق فیدخوانی و send_message به چت‌های ذخیره شده قرار گیرد.
    # مثال:
    # news_content = get_ai_news()
    # await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=news_content)
    logging.info("Running daily news job.")
    pass


def init_app(token: str) -> Application:
    """راه‌اندازی Application برای محیط Webhook"""
    app = Application.builder().token(token).build()

    # اضافه کردن فرمان /start
    app.add_handler(CommandHandler("start", start))

    # JobQueue برای ارسال خبر روزانه ساعت 9 صبح
    job_queue: JobQueue = app.job_queue
    # دقت کنید: اگر تابع send_news منطق کامل نداشته باشد، این بخش فقط لاگ می‌گیرد.
    job_queue.run_daily(send_news, time=time(hour=9, minute=0, second=0))

    return app
