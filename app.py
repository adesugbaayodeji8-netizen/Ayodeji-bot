import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# --- READ TOKEN FROM ENVIRONMENT ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    logging.error("❌ TELEGRAM_TOKEN is NOT SET in environment variables!")
else:
    logging.info("✅ Token loaded successfully.")

# --- FLASK ROUTE ---
@app.route('/')
def home():
    return "✅ Bot is running!"

@app.route('/health')
def health():
    return "OK"

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

# --- BOT STARTER ---
def run_telegram_bot():
    if not TOKEN:
        logging.error("❌ Bot cannot start because TOKEN is missing!")
        return
    
    try:
        logging.info("🤖 Telegram bot is starting...")
        bot_app = Application.builder().token(TOKEN).build()
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        logging.info("✅ Telegram bot is now polling...")
        bot_app.run_polling()
    except Exception as e:
        logging.error(f"❌ Bot crashed: {e}")

# --- MAIN ---
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"🚀 Flask running on port {port}...")
    app.run(host="0.0.0.0", port=port)
