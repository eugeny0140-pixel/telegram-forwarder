import os
from telegram.ext import Application, MessageHandler, filters

SOURCE = "@time_n_John"
TARGET = "@finanosint"
BOT_TOKEN = os.getenv("FORWARDER_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("FORWARDER_BOT_TOKEN не задан")

async def forward(update, context):
    msg = update.channel_post
    if not msg:
        return
    chat = msg.chat
    username = f"@{chat.username}" if chat.username else str(chat.id)
    if username != SOURCE and str(chat.id) != SOURCE:
        return
    try:
        await context.bot.forward_message(TARGET, chat.id, msg.message_id)
        print(f"✅ Переслано: {msg.message_id}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward))
    print("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
