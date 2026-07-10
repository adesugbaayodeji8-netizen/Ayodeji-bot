import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("8373826607:AAGNafN7e8Q8822w9PfYdeuuPa9ayEHWhaQ")  # Render will set this

# --- FLASK WEB SERVER (Keeps Render happy) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Academic Bot is running!"

@app.route('/health')
def health():
    return "OK"

# --- TELEGRAM BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **Welcome to your Academic Study Bot!**\n\n"
        "I can help you with:\n"
        "📖 Answer questions from your textbooks\n"
        "🧠 Quiz you with flashcards\n"
        "🔍 Search for images and explanations\n"
        "⏰ Send study reminders\n\n"
        "Send me a PDF to get started!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"👋 Hi {user_name}! You said: {user_text}")

def run_telegram_bot():
    """Runs the Telegram bot in a background thread."""
    tg_app = Application.builder().token(TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("🤖 Telegram bot is running...")
    tg_app.run_polling()

# --- MAIN ---
if __name__ == "__main__":
    # Start Telegram bot in background
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()
    
    # Start Flask web server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
