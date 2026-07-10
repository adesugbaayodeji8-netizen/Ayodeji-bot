import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIG ---
logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    logging.error("❌ Token missing!")
    exit(1)

flask_app = Flask(__name__)

# --- TELEGRAM BOT SETUP ---
bot_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is finally live! Send me any text.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --- WEBHOOK ROUTE (This replaces polling) ---
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        asyncio.run(bot_app.process_update(update))
        return "OK", 200
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "ERROR", 500

@flask_app.route('/')
def home():
    return "Bot is ready!"

# --- MAIN ---
if __name__ == "__main__":
    # Set the webhook on startup
    hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if hostname:
        webhook_url = f"https://{hostname}/webhook"
        logging.info(f"🔗 Setting webhook to: {webhook_url}")
        asyncio.run(bot_app.bot.set_webhook(webhook_url))
        logging.info("✅ Webhook set successfully!")
    else:
        logging.warning("⚠️ Hostname not found. Webhook not set.")

    # Start Flask server (no threads, no polling)
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
