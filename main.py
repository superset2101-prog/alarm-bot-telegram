from telegram.ext import Updater, CommandHandler
import datetime
import threading
import os

TOKEN = os.getenv("TOKEN")

def start(update, context):
    update.message.reply_text("Привет! Я будильник. Напиши /alarm 07:30")

def alarm(update, context):
    try:
        if len(context.args) != 1:
            update.message.reply_text("Формат: /alarm 07:30")
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
        update.message.reply_text(f"Будильник установлен на {alarm_time.strftime('%H:%M')}")

    except Exception as e:
        update.message.reply_text("Ошибка. Формат: /alarm 07:30")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("alarm", alarm))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
