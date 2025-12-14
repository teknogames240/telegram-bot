
import feedparser
import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO)

TOKEN = "7256343666:AAGHKZDpAQe3hrAj99hULLJCS-1SZULumMs"

RSS_SOURCES = [
    "https://ai.googleblog.com/feeds/posts/default",
    "https://openai.com/blog/rss.xml",
    "https://venturebeat.com/ai/feed/",
    "https://digiato.com/feed",
]

def get_ai_news():
    news = []

    for url in RSS_SOURCES:
        feed = feedparser.parse(url)
        for entry in feed.entries[:2]:
            title = entry.title
            link = entry.link
            news.append(f"🧠 {title}\n🔗 {link}")

    return news[:5]

def start(update, context):
    news = get_ai_news()

    if news:
        message = "📰 آخرین اخبار هوش مصنوعی:\n\n" + "\n\n".join(news)
    else:
        message = "❌ خبری پیدا نشد"

    update.message.reply_text(message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()
# bot.py (تغییرات کلیدی)
# ... (کدهای import و توابع get_ai_news و send_news و start دست نخورده باقی می‌مانند)

# تابع جدید برای راه‌اندازی ربات
def init_app(token: str) -> Application:
    # ۱. ساخت برنامه (Application)
    app = Application.builder().token(token).build()

    # ۲. اضافه کردن فرمان /start
    app.add_handler(CommandHandler("start", start))

    # ۳. JobQueue برای ارسال خبر روزانه ساعت 9 صبح
    job_queue: JobQueue = app.job_queue
    # JobQueue در حالت Webhook کار می‌کند، اما اگر سرویس Render به خواب برود، ممکن است اعلان را از دست بدهد.
    job_queue.run_daily(send_news, time=time(hour=9, minute=0))
    
    return app



