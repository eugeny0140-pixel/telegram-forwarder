import os
import logging
from telegram.ext import Application, MessageHandler, filters

# === Настройки ===
SOURCE = "@time_n_John"          # Публичный канал-источник (можно заменить на ID)
TARGET = "6957643599"           # Приватный канал-получатель (ID без @)
BOT_TOKEN = os.getenv("FORWARDER_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Переменная FORWARDER_BOT_TOKEN не задана")

# === Логирование ===
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def forward(update, context):
    msg = update.channel_post
    if not msg:
        return

    chat = msg.chat
    expected_username = SOURCE.lstrip('@')
    # Поддержка как username, так и числового ID источника
    if chat.username != expected_username and str(chat.id) != SOURCE:
        return

    try:
        # Копируем сообщение — без упоминания отправителя
        await context.bot.copy_message(
            chat_id=TARGET,
            from_chat_id=msg.chat.id,
            message_id=msg.message_id,
            caption=msg.caption if msg.caption else None,
            parse_mode="HTML"
        )
        logger.info(f"✅ Скопировано (скрыто): {msg.message_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка при копировании: {e}", exc_info=True)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward))
    logger.info("🚀 Бот запущен и ожидает сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()
