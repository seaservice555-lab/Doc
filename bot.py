import os
import sys
import logging
from datetime import datetime, timedelta
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from gcal_client import GoogleCalendarClient

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой бот-календарь.")

async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    logger.info("Бот запускается на сервере...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот успешно запущен!")

    # Держим бота запущенным
    import asyncio
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
