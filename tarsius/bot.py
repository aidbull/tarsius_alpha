from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Updater, Filters, MessageHandler
from telegram.utils.request import Request
from data_base import create_new_worker, get_details_for_task, save_comment_from_user, get_status


start_words = ['start', 'Start', '/start', '/Start', 'START', '/START']
button_help = 'Моя задача'
button_get_comment_yes = 'Успеваю'
button_get_comment_risk = 'Есть риск'
button_get_comment_no = 'Не успеваю'
button_get_status = 'Статус по проекту'
admin_uid = 'UID Админа'

# обработка кнопок с комментариями от дизайнеров
def button_help_handler(update: Update, context: CallbackContext,):

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_get_comment_yes),
            ],
            [
                KeyboardButton(text=button_get_comment_risk),
            ],
            [
                KeyboardButton(text=button_get_comment_no),
            ],
        ],
        resize_keyboard=True,
    )

    user = update.message.from_user
    user_username = user['username']
    print('username to send to DB ', user_username)
    name, project_name, task, deadline, link_to_TZ = get_details_for_task(user_username)
    print('Got info from DB: ', name, project_name, task, deadline, link_to_TZ)
    update.message.reply_text(
        text='Привет, {}.\nВ проекте "{}" твоя задача:\n"{}"\nВсе детали и ТЗ ты найдешь по этой ссылке:\n{}\n\nВАЖНО: дедлайн {}'.format(name, project_name, task, link_to_TZ, deadline),
        reply_markup=reply_markup,
    )


# обработка кнопки для получения дизайнером своей задачи
def button_status_handler(update: Update, context: CallbackContext,):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_get_status),
            ],
        ],
        resize_keyboard=True,
    )
    text = get_status()
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
    )


# обработка реакции на комментарий дизайнера по успеваемости
def button_get_comment_handler(update: Update, context: CallbackContext,):

    text = update.message.text
    comment_from_user = text
    user = update.message.from_user
    user_username = user['username']
    print('username: {}, text: {}'.format(user_username, comment_from_user))

    if text == button_get_comment_yes:
        update.message.reply_text(
            text='Красава',
            reply_markup=ReplyKeyboardRemove(),
        )

    elif text == button_get_comment_risk:
        update.message.reply_text(
            text='Напрягись там, нормально сделай!',
            reply_markup=ReplyKeyboardRemove(),
        )

    elif text == button_get_comment_no:
        update.message.reply_text(
            text='Ну пиздец тебе',
            reply_markup=ReplyKeyboardRemove(),
        )

    save_comment_from_user(user_username, text)


# основной обработчик
def message_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id == admin_uid:
        text = update.message.text
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=button_get_status),
                ],
            ],
            resize_keyboard=True,
        )

        update.message.reply_text(
            text='Узнать статус по проектам?',
            reply_markup=reply_markup,
        )

        if text == button_get_status:
            return button_status_handler(update=update, context=context)


    else:
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=button_help),
                ],
            ],
            resize_keyboard=True,
        )

        text = update.message.text
        user = update.message.from_user
        user_id = user['id']
        user_username = user['username']
        #chat_id = update.message.chat_id

        if text == button_help:
            return button_help_handler(update=update, context=context)

        elif text == button_get_comment_yes or text == button_get_comment_risk or text == button_get_comment_no:
            button_get_comment_handler(update=update, context=context)

        elif text in start_words:
            respond = create_new_worker(user_id, user_username, chat_id)
            print('You talk with user {} and his user ID: {} , the chat ID: {}\nThis user is already in the database: {}'.format(user_username, user_id, chat_id, respond))
            if respond == 'yes':
                update.message.reply_text(text='Привет, {}!\nЯ бот Тарсиус.\nУточняю твою задачу и скоро вернусь с деталями по проекту.'.format(user_username), reply_markup=reply_markup)
            elif respond == 'no':
                update.message.reply_text(text='Привет!\nНе нашел твой user_id в списке задач по нашим проектам.',)

        else:
            update.message.reply_text(text='Если нужно меня включить, напишите start')



def main():
    print('Start')

    req = Request(
        connect_timeout=0.5,
    )

    bot = Bot(
        request=req,
        token='',
    )

    updater = Updater(
        bot=bot,
        use_context=True,
    )

    print(updater.bot.get_me())

    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()

    print('Finish')

if __name__ == '__main__':
    main()