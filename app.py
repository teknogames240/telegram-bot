# app.py
import os
from flask import Flask, request, abort
from telegram.ext import Application
from bot import init_app # فرض می‌کنیم تابع main در bot.py را به init_app تغییر می‌دهید

# توکن و URLها از متغیرهای محیطی
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
URL = os.environ.get("RENDER_EXTERNAL_URL") 
PORT = int(os.environ.get("PORT", "5000"))

if not TOKEN or not URL:
    raise ValueError("TELEGRAM_BOT_TOKEN and RENDER_EXTERNAL_URL must be set.")

app = Flask(__name__)

# ۱. راه‌اندازی ربات
application = init_app(TOKEN) # اجرای JobQueue و Handlers

# ۲. تنظیم Webhook
@app.route('/', methods=['GET'])
def home():
    return "AI News Bot is running!", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """هندل کردن درخواست‌های Webhook از تلگرام"""
    if request.method == "POST":
        update = request.get_json(force=True)
        # پردازش آپدیت توسط Application
        application.update_queue.put(update)
        return "ok"
    return abort(400)

# ۳. تنظیم Webhook در تلگرام هنگام راه‌اندازی
def set_webhook():
    webhook_url = f"{URL}/{TOKEN}"
    print(f"Setting webhook to: {webhook_url}")
    # Application.set_webhook() را به صورت دستی یا هنگام ساخت سرویس اجرا کنید.
    # به دلیل اینکه Render آدرس را تغییر می‌دهد، بهتر است آن را در محیط Render اجرا کنید.

if __name__ == '__main__':
    # این فقط برای تست لوکال است
    app.run(debug=True, port=PORT)
