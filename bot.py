import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from utils import detect_chain
from scan_engine import scan_token

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Memecoin Risk Scanner\n\nUse:\n/scan <token_address>"
    )


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /scan <token_address>")
        return

    address = context.args[0]

    if not detect_chain(address):
        await update.message.reply_text("❌ Invalid token address.")
        return

    await update.message.reply_text("🔍 Scanning token...")

    try:
        result = scan_token(address)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("⚠️ Scan failed. Try again later.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    print("Bot running locally...")
    app.run_polling()


# allow external start (Render thread)
def start():
    main()

# allow external start (Render thread)
def start():
    main()

if __name__ == "__main__":
    main()

