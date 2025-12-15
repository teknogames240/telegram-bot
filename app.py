import os
from flask import Flask, request, abort
from telegram.ext import Application
from bot import init_app # فراخوانی تابع راه‌اندازی ربات

# توکن و URLها از متغیرهای محیطی
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
URL = os.environ.get("RENDER_EXTERNAL_URL") 
# پورت باید 10000 باشد
PORT = int(os.environ.get("PORT", "10000")) 

# این چک کردن باعث توقف Deploy می‌شد، اما اگر توکن در Render تنظیم شده باشد، اکنون مشکلی نیست.
if not TOKEN or not URL:
    raise ValueError("TELEGRAM_BOT_TOKEN and RENDER_EXTERNAL_URL must be set.")

app = Flask(__name__)

# ۱. راه‌اندازی ربات
application = init_app(TOKEN) # اجرای JobQueue و Handlers

# ۲. تعریف روت‌های Flask
@app.route('/', methods=['GET'])
def home():
    """روت اصلی برای چک کردن وضعیت سرویس توسط Render"""
    return "AI News Bot is running!", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """هندل کردن درخواست‌های Webhook از تلگرام"""
    if request.method == "POST":
        # دریافت آپدیت JSON از تلگرام
        update_json = request.get_json(force=True)
        
        # پردازش آپدیت توسط Application
        # اینجا باید مطمئن شویم که داده JSON به درستی به شیء Update تبدیل شود.
        try:
            from telegram import Update
            update = Update.de_json(update_json, application.bot)
            application.process_update(update)
        except Exception as e:
            # اگر خطایی در پردازش رخ داد، آن را لاگ کنید
            print(f"Error processing update: {e}")
            
        return "ok"
    return abort(400)

if __name__ == '__main__':
    # این فقط برای تست لوکال است
    app.run(debug=True, port=PORT)
