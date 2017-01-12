# LyceumTIUbot

import telebot
import answers
import constants
import json

bot = telebot.TeleBot(constants.token)
schedule_type_queue = []
schedule_day_queue = []
schedule_group_queue = []
schedule_user_type = {}
schedule_user_day = {}
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


def load_schedule(_type="1"):
    with open("schedule{0}.json".format(_type), 'r', encoding='UTF8') as schedule_data:
        file = schedule_data.read().replace('\n', '')
        data = json.loads(file)
    return data

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
    # HANDLING THE SECOND STEP
    if message.from_user.id in schedule_type_queue:
        if message.text in constants.schedule_types:
            schedule_user_type[message.from_user.id] = constants.schedule_types.index(message.text)
            schedule_day_queue.append(message.from_user.id)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            user_markup.row('Понедельник', 'Вторник', 'Среда')
            user_markup.row('Четверг', 'Пятница', 'Суббота')
            bot.send_message(message.from_user.id, answers.schedule_day, reply_markup=user_markup)
            answer = answers.schedule_day + "\nДобавлен в лист ожидания ответа."
        else:
            answer = "НЕТ ТАКОГО ТИПА РАСПИСАНИЯ!"
            bot.send_message(message.from_user.id, answer)
        schedule_type_queue.remove(message.from_user.id)
    elif message.from_user.id in schedule_day_queue:
        if message.text in constants.schedule_days:
            schedule_user_day[message.from_user.id] = message.text
            schedule_group_queue.append(message.from_user.id)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            user_markup.row("101", "102", "103", "104")
            user_markup.row("111", "112", "113", "114")
            bot.send_message(message.from_user.id, answers.schedule_group, reply_markup=user_markup)
            answer = answers.schedule_group + "\nДобавлен в лист ожидания ответа."
        else:
            answer = "НЕТ ТАКОГО ДНЯ НЕДЕЛИ!"
        schedule_day_queue.remove(message.from_user.id)
    elif message.from_user.id in schedule_group_queue:
        if message.text in constants.groups:
            schedule = load_schedule(str(schedule_user_type[message.from_user.id]+1))
            day = schedule_user_day.pop(message.from_user.id)
            stype = schedule_user_type.pop(message.from_user.id)
            answer = """Расписание {0} группы на {1} ({2})
1: {3}\n2: {4}\n3: {5}\n4: {6}""".format(message.text,
                                        day,
                                        constants.schedule_types[stype].lower(),
                                        schedule[message.text][day]["first"],
                                        schedule[message.text][day]["second"],
                                        schedule[message.text][day]["third"],
                                        schedule[message.text][day]["fourth"])
            bot.send_message(message.from_user.id, answer)
        else:
            answer = "НЕТ ТАКОЙ ГРУППЫ!"
        schedule_group_queue.remove(message.from_user.id)
    elif message.text.lower() == "как тебя зовут?":
        answer = answers.myname
        bot.send_message(message.from_user.id, answer)
    elif message.text == "Стив":
        answer = answers.steve
        bot.send_message(message.from_user.id, answer)
    # HANDLING THE FIRST STEP
    elif message.text == "Расписание":
        schedule_type_queue.append(message.from_user.id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Числитель', 'Знаменатель')
        user_markup.row('Последние изменения')
        bot.send_message(message.from_user.id, answers.schedule_type, reply_markup=user_markup)
        answer = answers.schedule_type + "\nДобавлен в лист ожидания ответа."
    else:
        answer = answers.cant_understand
        bot.send_message(message.from_user.id, answer)
    log(message, answer)
bot.polling(none_stop=True, interval=0)
