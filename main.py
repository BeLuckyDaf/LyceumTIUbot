# LyceumTIUbot

import telebot
import answers
import constants
import json


bot = telebot.TeleBot(constants.token)
new_last_changes_queue = []
schedule_type_queue = []
schedule_day_queue = []
schedule_group_queue = []
schedule_user_type = {}
schedule_user_day = {}
last_changes_id = "0"


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
    if _type == "1" or _type == "2":
        with open(constants.schedule_file_path.format(_type), 'r', encoding='UTF8') as schedule_data:
            file = schedule_data.read().replace('\n', '')
            data = json.loads(file)
        return data
    else:
        print("VERY STUPID ERROR!\nHOW COULD YOU NOT FIX IT?!")
        exit()


# First handle all commands available and show the menu
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/about', '/help', '/stop')
    user_markup.row('Расписание', 'Как тебя зовут?')
    bot.send_message(message.from_user.id, 'Я рад, что ты к нам присоединился!\nМеню создано.',
                     reply_markup=user_markup)
    log(message, "Меню создано.")


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Меню убрано.", reply_markup=hide_markup)
    log(message, "Меню убрано.")


@bot.message_handler(commands=['setlast'])
def handle_setlast(message):
    if message.from_user.id in constants.admins:
        new_last_changes_queue.append(message.from_user.id)
        answer = "Загрузите новые последние изменения:"
    else:
        answer = "Только админ и его приближённые способны на такое!"
    bot.send_message(message.from_user.id, answer)
    log(message, answer)


@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.from_user.id, answers.aboutme)
    log(message, answers.aboutme)


@bot.message_handler(commands=['help'])
def handle_about(message):
    bot.send_message(message.from_user.id, answers.list_commands)
    log(message, answers.list_commands)


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    if message.from_user.id in new_last_changes_queue:
        new_last_changes_queue.remove(message.from_user.id)
        global last_changes_id
        last_changes_id = str(message.photo[-1].file_id)
        answer = "Принял файл... Наверное..."
        bot.send_message(message.from_user.id, answer)
        log(message, answer)


# Then texts
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # HANDLING SCHEDULE REQUEST (DAY OF A WEEK)
    if message.from_user.id in schedule_type_queue:
        if message.text in constants.schedule_types:
            schedule_user_type[message.from_user.id] = constants.schedule_types.index(message.text)
            # IF LAST CHANGES:
            if constants.schedule_types.index(message.text) == 2:
                schedule_type_queue.remove(message.from_user.id)
                if last_changes_id == "0":
                    answer = "Я пока не знаю изменений..."
                    bot.send_message(message.from_user.id, answer)
                else:
                    bot.send_photo(message.from_user.id, last_changes_id)
                    answer = "Попытались отправить фото, надеемся, получилось."
                log(message, answer)
                return
            # END IF
            else:
                schedule_day_queue.append(message.from_user.id)
                user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
                user_markup.row('Понедельник', 'Вторник')
                user_markup.row('Среда', 'Четверг')
                user_markup.row('Пятница', 'Суббота')
                bot.send_message(message.from_user.id, answers.schedule_day, reply_markup=user_markup)
                answer = answers.schedule_day + "\nДобавлен в лист ожидания ответа."
        else:
            answer = "НЕТ ТАКОГО ТИПА РАСПИСАНИЯ!"
            bot.send_message(message.from_user.id, answer)
        schedule_type_queue.remove(message.from_user.id)
    # HANDLING SCHEDULE REQUEST (GROUP)
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
    # HANDLING SCHEDULE REQUEST (ASSEMBLING THE MESSAGE AND SENDING IT)
    elif message.from_user.id in schedule_group_queue:
        if message.text in constants.groups:
            if schedule_user_type[message.from_user.id] < 2:
                schedule = load_schedule(str(schedule_user_type[message.from_user.id] + 1))
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
        else:
            answer = "НЕТ ТАКОЙ ГРУППЫ!"
        bot.send_message(message.from_user.id, answer)
        schedule_group_queue.remove(message.from_user.id)
    elif message.text.lower() == "как тебя зовут?":
        answer = answers.myname
        bot.send_message(message.from_user.id, answer)
    elif message.text == "Стив":
        answer = answers.steve
        bot.send_message(message.from_user.id, answer)
    # HANDLING SCHEDULE REQUEST (SCHEDULE TYPE)
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
