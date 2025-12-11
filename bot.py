import telegram
from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup
from telegram.ext import JobQueue
import os
from datetime import time
import re
from urllib.parse import parse_qs, urlparse

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')
# Telegram Chat ID
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_TELEGRAM_CHAT_ID')

def get_ai_news():
    """
    Searches Google for AI news and returns a list of headlines and links.
    """
    url = "https://www.google.com/search?q=AI+news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news = []
    for a in soup.find_all('a', href=re.compile(r'/url\?q=')):
        if a.h3:
            title = a.h3.text
            href = a['href']
            parsed_url = urlparse(href)
            actual_link = parse_qs(parsed_url.query).get('q', [None])[0]
            
            if actual_link:
                news.append(f"{title}\n{actual_link}\n")
    return news

def send_news(context):
    """
    Sends the AI news to the specified Telegram chat.
    """
    news = get_ai_news()
    if news:
        message = "AI News Update:\n\n" + "\n".join(news[:5])
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    else:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="No AI news found.")

def start(update, context):
    """
    Starts the bot and sends a welcome message.
    """
    update.message.reply_text('Welcome to the AI News Bot! I will send you AI news updates periodically.')

def main():
    """
    Main function to run the bot.
    """
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Add the start command handler
    dp.add_handler(CommandHandler("start", start))
    
    # Schedule the news to be sent every day at 09:00
    job_queue = updater.job_queue
    job_queue.run_daily(send_news, time=time(hour=9, minute=0))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
