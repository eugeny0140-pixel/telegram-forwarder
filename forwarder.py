import os
from telegram.ext import Application, MessageHandler, filters

# === НАСТРОЙКИ ===
SOURCE_CHANNEL = "@time_n_John"      # Имя или ID канала-источника
TARGET_CHANNEL = "@finanosint"       # Имя или ID канала-назначения
BOT_TOKEN = os.getenv("FORWARDER_BOT_TOKEN")  # Токен бота-пересылателя

if not BOT_TOKEN:
    raise ValueError("Установите переменную окружения FORWARDER_BOT_TOKEN")

async def forward_message(update, context):
    msg = update.channel_post
    if not msg:
        return

    # Проверяем, что сообщение пришло именно из нужного канала
    chat_id = str(msg.chat.id)
    chat_username = f"@{msg.chat.username}" if msg.chat.username else ""

    if chat_username != SOURCE_CHANNEL and chat_id != SOURCE_CHANNEL:
        return

    try:
        await context.bot.forward_message(
            chat_id=TARGET_CHANNEL,
            from_chat_id=msg.chat.id,
            message_id=msg.message_id
        )
        print(f"✅ Переслано сообщение {msg.message_id} из {chat_username or chat_id}")
    except Exception as e:
        print(f"❌ Ошибка при пересылке: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward_message))
    print("🚀 Бот запущен. Ожидание сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()
