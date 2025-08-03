from telegram.ext import ApplicationBuilder, CommandHandler
import datetime
import threading
import os

TOKEN = os.getenv("TOKEN")

async def start(update, context):
    await update.message.reply_text("Привет! Я будильник. Напиши /alarm 07:30")

async def alarm(update, context):
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Формат: /alarm 07:30")
            return

        user_time = context.args[0]
        alarm_time = datetime.datetime.strptime(user_time, "%H:%M").time()
        now = datetime.datetime.now()
        alarm_datetime = datetime.datetime.combine(now.date(), alarm_time)

        if alarm_datetime <= now:
            alarm_datetime += datetime.timedelta(days=1)

        delay = (alarm_datetime - now).total_seconds()
        chat_id = update.message.chat_id

        def send_alarm():
            context.bot.send_message(chat_id=chat_id, text="🔔 Пора просыпаться!")

        threading.Timer(delay, send_alarm).start()
        await update.message.reply_text(f"Будильник установлен на {alarm_time.strftime('%H:%M')}")

    except Exception as e:
        await update.message.reply_text("Ошибка. Формат: /alarm 07:30")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("alarm", alarm))

    app.run_polling()

if __name__ == '__main__':
    main()
