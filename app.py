import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from bot import build_application, set_webhook

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN or not RENDER_URL:
    raise RuntimeError("Environment variables not set")

app = Flask(__name__)

# ساخت Application تلگرام
application: Application = build_application(TOKEN)

# ست کردن Webhook هنگام بالا آمدن
set_webhook(TOKEN, f"{RENDER_URL}/{TOKEN}")

@app.route("/", methods=["GET"])
def home():
    return "Telegram bot is running ✅", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
