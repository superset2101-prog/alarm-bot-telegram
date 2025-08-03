from telegram.ext import Application, CommandHandler
import os

async def start(update, context):
    await update.message.reply_text("Привет! Я твой бот.")

def main():
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # Настройка webhook
    port = int(os.getenv("PORT", 8443))  # Render использует переменную PORT
    webhook_url = os.getenv("WEBHOOK_URL")  # Например, https://your-app.onrender.com
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=token,
        webhook_url=f"{webhook_url}/{token}"
    )

if __name__ == "__main__":
    main()
