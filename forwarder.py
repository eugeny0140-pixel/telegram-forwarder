import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL", "@time_n_John")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "@finanosint")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    if not message:
        return

    # Проверяем, что сообщение из нужного канала
    chat_username = message.chat.username
    if f"@{chat_username}" != SOURCE_CHANNEL:
        return

    try:
        # Пересылаем сообщение как есть (сохраняя форматирование, фото, ссылки)
        await context.bot.forward_message(
            chat_id=TARGET_CHANNEL,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )
        logger.info(f"✅ Переслано: {message.message_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.CHANNEL_POSTS, forward_message))
    logger.info(f"🚀 Бот запущен. Мониторинг {SOURCE_CHANNEL} → {TARGET_CHANNEL}")
    application.run_polling()

if __name__ == "__main__":
    main()
