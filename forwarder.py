import os
import logging
from telegram.ext import Application, MessageHandler, filters

SOURCE = "@time_n_John"
TARGET = "-2914190770"
BOT_TOKEN = os.getenv("FORWARDER_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("FORWARDER_BOT_TOKEN не задан")

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
    logger.info("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
