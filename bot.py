import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from scanner import scan_token

BOT_TOKEN = os.getenv("BOT_TOKEN")


# ======================
# Commands
# ======================

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Memecoin Risk Scanner\n\n"
        "Use:\n"
        "/scan <token_address>"
    )


async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /scan <token_address>")
        return

    address = context.args[0]

    msg = await update.message.reply_text("🔍 Scanning token...")

    try:
        result = await scan_token(address)
        await msg.edit_text(result)

    except Exception as e:
        print("SCAN ERROR:", e)
        await msg.edit_text("⚠️ Scan failed. Try again later.")


# ======================
# Main bot loop
# ======================

async def run():
    print("🚀 BOT STARTING...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("scan", scan_cmd))

    print("✅ Polling started")
    await app.run_polling()


def start():
    asyncio.run(run())


if __name__ == "__main__":
    start()
