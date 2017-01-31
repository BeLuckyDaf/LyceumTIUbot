#!/usr/bin/python3
# LyceumTIUbot

import telebot
import answers
import constants
import json_file
import usermgr
import cherrypy
import logging

# Class objects
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(constants.token)
schedule_data = json_file.JsonFile("schedule1.json")
users_data = json_file.JsonFile(constants.users_path)
# Lists and variables / queues
hide_markup = telebot.types.ReplyKeyboardRemove()
# new_last_changes_ten_queue = []
# new_last_changes_eleven_queue = []
# lastch_type_queue = []
# lastch_settype_queue = []
# schedule_type_queue = []
# schedule_day_queue = []
# schedule_group_queue = []
schedule_user_type = {}
schedule_user_day = {}
last_changes_id = ["0", "0"]
queue = {"new_last_changes_ten": [], "new_last_changes_eleven": [], "lastch_type": [],
         "lastch_settype": [], "schedule_type": [], "schedule_day": [], "schedule_group": [],
         "newadmin": [], "newsub": [], "newmoder": []}


# WebhookServer, process webhook calls
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


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
        schedule_data.setpath(constants.schedule_path.format(_type))
        data = schedule_data.getcontents()
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
    bot.send_message(message.from_user.id, "Меню убрано.", reply_markup=hide_markup)
    log(message, "Меню убрано.")


@bot.message_handler(commands=['newadmin'])
def handle_newadmin(message):
    if usermgr.isadmin(users_data, message.from_user.id):
        queue["newadmin"].append(message.from_user.id)
        send_message(message.from_user.id, "Отправь контакт нового админа: ")


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.from_user.id in queue["newadmin"]:
        queue["newadmin"].remove(message.from_user.id)
        usermgr.adduser(users_data, message.contact.user_id)
    elif message.from_user.id in queue["newsub"]:
        queue["newsub"].remove(message.from_user.id)
        usermgr.adduser(users_data, message.contact.user_id)
    elif message.from_user.id in queue["newmoder"]:
        queue["newmoder"].remove(message.from_user.id)
        usermgr.adduser(users_data, message.contact.user_id) 


@bot.message_handler(commands=['setlast'])
def handle_setlast(message):
    if usermgr.isadmin(users_data, message.from_user.id):
        queue["lastch_settype"].append({"id": message.from_user.id})
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('10', '11')
        answer = "Выбери группу:"
        bot.send_message(message.from_user.id, answer, reply_markup=user_markup)
    else:
        answer = """Только админ и его приближённые способны на такое!
Забудь, что написал это, смертный! Я тоже притворюсь, будто не видел.
Согласен? Вот и отлично!
...Хееееей! Чем могу помочь?"""
        bot.send_message(message.from_user.id, answer)
    log(message, answer)


@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.from_user.id, answers.aboutme)
    log(message, answers.aboutme)
# def handle_about(message):
#    bot.send_message(message.from_user.id, answers.aboutme)
#    log(message, answers.aboutme)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.from_user.id, answers.list_commands)
    log(message, answers.list_commands)


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    global last_changes_id
    if {"id": message.from_user.id} in queue["new_last_changes_ten"]:
        queue["new_last_changes_ten"].remove({"id": message.from_user.id})
        last_changes_id[0] = str(message.photo[-1].file_id)
        answer = "Принял файл! Последние изменения обновлены!"
        bot.send_message(message.from_user.id, answer)
        log(message, answer)
    elif {"id": message.from_user.id} in queue["new_last_changes_eleven"]:
        queue["new_last_changes_eleven"].remove({"id": message.from_user.id})
        last_changes_id[1] = str(message.photo[-1].file_id)
        answer = "Принял файл! Последние изменения обновлены!"
        bot.send_message(message.from_user.id, answer)
        log(message, answer)


# Then texts
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_text(message):
    answer = ""
    if {"id": message.from_user.id} in queue["lastch_settype"]:
        queue["lastch_settype"].remove({"id": message.from_user.id})
        if (message.text == "10"):
            queue["new_last_changes_ten"].append({"id": message.from_user.id})
            answer = "Загружай:"
            bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
        elif (message.text == "11"):
            queue["new_last_changes_eleven"].append({"id": message.from_user.id})
            answer = "Загружай:"
            bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
        else:
            answer = "Лол..."
            bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
        log(message, answer)
    elif {"id":message.from_user.id} in queue["lastch_type"]:
        queue["lastch_type"].remove({"id":message.from_user.id})
        if (message.text == "10"):
            if last_changes_id[0] == "0":
                    answer = "Я пока не знаю изменений..."
                    bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
            else:
                    bot.send_chat_action(message.from_user.id, 'upload_photo')
                    bot.send_photo(message.from_user.id, last_changes_id[0], reply_markup=hide_markup)
                    answer = "Попытались отправить фото, надеемся, получилось."
                    log(message, answer)
        elif (message.text == "11"):
            if last_changes_id[1] == "0":
                    answer = "Я пока не знаю изменений..."
                    bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
            else:
                    bot.send_chat_action(message.from_user.id, 'upload_photo')
                    bot.send_photo(message.from_user.id, last_changes_id[1], reply_markup=hide_markup)
                    answer = "Попытались отправить фото, надеемся, получилось."
                    log(message, answer)
    # HANDLING SCHEDULE REQUEST (DAY OF A WEEK)
    elif {"id": message.from_user.id} in queue["schedule_type"]:
        if message.text in constants.schedule_types:
            schedule_user_type[message.from_user.id] = constants.schedule_types.index(message.text)
            # IF LAST CHANGES:
            if constants.schedule_types.index(message.text) == 2:
                queue["schedule_type"].remove({"id": message.from_user.id})
                queue["lastch_type"].append({"id": message.from_user.id})
                user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
                user_markup.row('10', '11')
                bot.send_message(message.from_user.id, answers.lastch_type, reply_markup=user_markup)
                answer = answers.lastch_type + "\nДобавлен в лист ожидания ответа."
                return
            # END IF
            else:
                queue["schedule_day"].append({"id": message.from_user.id})
                queue["schedule_type"].remove({"id": message.from_user.id})
                user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
                user_markup.row('Понедельник', 'Вторник')
                user_markup.row('Среда', 'Четверг')
                user_markup.row('Пятница', 'Суббота')
                bot.send_message(message.from_user.id, answers.schedule_day, reply_markup=user_markup)
                answer = answers.schedule_day + "\nДобавлен в лист ожидания ответа."
        else:
            answer = "НЕТ ТАКОГО ТИПА РАСПИСАНИЯ!"
            bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
            queue["schedule_type"].remove({"id": message.from_user.id})
    # HANDLING SCHEDULE REQUEST (GROUP)
    elif {"id": message.from_user.id} in queue["schedule_day"]:
        if message.text in constants.schedule_days:
            schedule_user_day[message.from_user.id] = message.text
            queue["schedule_group"].append({"id": message.from_user.id})
            queue["schedule_day"].remove({"id": message.from_user.id})
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            user_markup.row("101", "102", "103", "104")
            user_markup.row("111", "112", "113", "114")
            bot.send_message(message.from_user.id, answers.schedule_group, reply_markup=user_markup)
            answer = answers.schedule_group + "\nДобавлен в лист ожидания ответа."
        else:
            answer = "НЕТ ТАКОГО ДНЯ НЕДЕЛИ!"
            bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
            queue["schedule_day"].remove({"id": message.from_user.id})
    # HANDLING SCHEDULE REQUEST (ASSEMBLING THE MESSAGE AND SENDING IT)
    elif {"id": message.from_user.id} in queue["schedule_group"]:
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
        bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
        queue["schedule_group"].remove({"id": message.from_user.id})
    elif message.text.lower() == "как тебя зовут?":
        answer = answers.myname
        bot.send_message(message.from_user.id, answer)
    elif message.text == "Стив":
        answer = answers.steve
        bot.send_message(message.from_user.id, answer)
    # HANDLING SCHEDULE REQUEST (SCHEDULE TYPE)
    elif message.text == "Расписание":
        queue["schedule_type"].append({"id": message.from_user.id})
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Числитель', 'Знаменатель')
        user_markup.row('Последние изменения')
        bot.send_message(message.from_user.id, answers.schedule_type, reply_markup=user_markup)
        answer = answers.schedule_type + "\nДобавлен в лист ожидания ответа."
    else:
        answer = answers.cant_understand
        bot.send_message(message.from_user.id, answer)
    
    log(message, answer)

# Legacy
# bot.polling(none_stop=True, interval=0)

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=constants.WEBHOOK_URL_BASE+constants.WEBHOOK_URL_PATH,
                certificate=open(constants.WEBHOOK_SSL_CERT, 'r'))

# Start cherrypy server
cherrypy.config.update({
    'server.socket_host': constants.WEBHOOK_LISTEN,
    'server.socket_port': constants.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': constants.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': constants.WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), constants.WEBHOOK_URL_PATH, {'/': {}})

