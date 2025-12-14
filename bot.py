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

if __name__ == "__main__":
    main()

