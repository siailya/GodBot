from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup


def start(update, context):
    reply_keyboard = [['Зайти в музей']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Привет! Отвечать вам будет живой человек!',
                              reply_markup=markup)


def task(context):
    job = context.job
    global length
    with open('from_vk_to_tg.txt', 'r') as logs:
        answers = logs.readlines()
        if len(answers) != length:
            context.bot.send_message(job.context, text=' '.join(answers[0].split()[:-4]))
            length += 1
        if answers:
            answers.pop(0)
            length -= 1
    with open('from_vk_to_tg.txt', 'w') as logs:
        logs.write(''.join(answers))


def send_message(update, context):
    chat_id = update.message.chat_id
    try:
        due = 1
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_repeating(task, due, context=chat_id)
        context.chat_data['job'] = new_job

    except (IndexError, ValueError):
        pass


def main():
    REQUEST_KWARGS = {
        'proxy_url': 'socks5h://geek:socks@t.geekclass.ru:7777'
    }
    updater = Updater("1156438301:AAFDrWFKvxh3zQFoHWh6trKSii8CVoODdbw", use_context=True,
                      request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, send_message)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(text_handler)
    print('Telegram bot started')
    updater.start_polling()
    updater.idle()


length = 0
if __name__ == '__main__':
    main()
