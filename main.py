# LyceumTIUbot

import telebot
import answers
import constants

bot = telebot.TeleBot(constants.token)

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
    log(message, "Меню убрано.")

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
    answer = answers.cant_understand
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.from_user.id, answers.myname)
        answer = answers.myname
    elif message.text == "Стив":
        bot.send_message(message.from_user.id, answers.steve)
        answer = answers.steve
    # TODO: Расписание!
    elif message.text == "Расписание":
        bot.send_message(message.from_user.id, answers.in_development)
        answer = answers.in_development
    else:
        bot.send_message(message.from_user.id, answers.cant_understand)
        answer = answers.cant_understand
    log(message, answer)
bot.polling(none_stop=True, interval=0)
