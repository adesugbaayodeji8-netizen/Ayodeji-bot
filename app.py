import os
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    logging.error("❌ TOKEN MISSING!")
    exit(1)

# --- FLASK ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running!"

# --- TELEGRAM ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Welcome! I am alive and listening!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    text = update.message.text
    await update.message.reply_text(f"👋 Hi {name}! You said: {text}")

# --- MAIN ---
def main():
    logging.info("🤖 Starting bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    logging.info("✅ Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    # Run Flask in a separate thread
    import threading
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()
    main()
