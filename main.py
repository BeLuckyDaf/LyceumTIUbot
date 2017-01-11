# LyceumTIUbot

import telebot
import answers
import constants

bot = telebot.TeleBot(constants.token)
schedule_queue = []

print(bot.get_me())


def log(message, answer):
    print("\n\t------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nТекст: {3}".format(message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 str(message.from_user.id),
                                                                 message.text))
    print("Ответ: {0}".format(answer))


# First handle all commands available and show the menu
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/about', '/help', '/stop')
    user_markup.row('Расписание', 'Как тебя зовут?')
    bot.send_message(message.from_user.id, 'Я рад, что ты к нам присоединился!\nМеню создано.', reply_markup=user_markup)
    log(message, "Меню создано.")


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Меню убрано.", reply_markup=hide_markup)
    log(message, "Меню убрано.")


@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.from_user.id, answers.aboutme)
    log(message, answers.aboutme)


@bot.message_handler(commands=['help'])
def handle_about(message):
    bot.send_message(message.from_user.id, answers.list_commands)
    log(message, answers.list_commands)


# Then texts
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.from_user.id in schedule_queue:
        if message.text == "101":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 101 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 101 ГРУППЫ!"
        elif message.text == "102":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 102 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 102 ГРУППЫ!"
        elif message.text == "103":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 103 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 103 ГРУППЫ!"
        elif message.text == "104":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 104 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 104 ГРУППЫ!"
        elif message.text == "111":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 111 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 111 ГРУППЫ!"
        elif message.text == "112":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 112 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 112 ГРУППЫ!"
        elif message.text == "113":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 113 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 113 ГРУППЫ!"
        elif message.text == "114":
            bot.send_message(message.from_user.id, "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 114 ГРУППЫ!")
            answer = "ЗДЕСЬ БУДЕТ РАСПИСАНИЕ 114 ГРУППЫ!"
        else:
            bot.send_message(message.from_user.id, "НЕТ ТАКОЙ ГРУППЫ!")
            answer = "НЕТ ТАКОЙ ГРУППЫ!"
        schedule_queue.remove(message.from_user.id)
    # answer = answers.cant_understand WHY IS IT NOT NEEDED?
    elif message.text.lower() == "как тебя зовут?":
        bot.send_message(message.from_user.id, answers.myname)
        answer = answers.myname
    elif message.text == "Стив":
        bot.send_message(message.from_user.id, answers.steve)
        answer = answers.steve
    # TODO: Расписание!
    elif message.text == "Расписание":
        schedule_queue.append(message.from_user.id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('101', '102', '103', '104')
        user_markup.row('111', '112', '113', '114')
        bot.send_message(message.from_user.id, answers.schedule, reply_markup=user_markup)
        answer = answers.schedule + "\nДобавлен в лист ожидания ответа."
    else:
        bot.send_message(message.from_user.id, answers.cant_understand)
        answer = answers.cant_understand
    log(message, answer)
bot.polling(none_stop=True, interval=0)
