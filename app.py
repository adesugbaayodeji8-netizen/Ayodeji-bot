import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO)

# --- READ TOKEN FROM ENVIRONMENT ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    logging.error("❌ TELEGRAM_TOKEN is NOT SET in environment variables!")
else:
    logging.info("✅ Token loaded successfully.")

# --- FLASK APP (Runs in a background thread) ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running!"

@flask_app.route('/health')
def health():
    return "OK"

def run_flask():
    """Runs Flask in a background thread."""
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"🚀 Flask server starting on port {port}...")
    flask_app.run(host="0.0.0.0", port=port)

# --- TELEGRAM HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **Welcome to your Academic Study Bot!**\n\n"
        "Send me any text and I will echo it back!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"👋 Hi {user_name}! You said: {user_text}")

# --- MAIN BOT FUNCTION (Runs in main thread) ---
def run_bot():
    if not TOKEN:
        logging.error("❌ Bot cannot start because TOKEN is missing!")
        return
    
    try:
        logging.info("🤖 Telegram bot is starting...")
        bot_app = Application.builder().token(TOKEN).build()
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        logging.info("✅ Telegram bot is now polling for messages...")
        bot_app.run_polling()
    except Exception as e:
        logging.error(f"❌ Bot crashed: {e}")

# --- MAIN ---
if __name__ == "__main__":
    # Start Flask in a background thread (safe to run here)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Run the Telegram bot in the MAIN thread (critical!)
    run_bot()
