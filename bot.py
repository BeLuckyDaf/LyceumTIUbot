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
cnslt_data = json_file.JsonFile("consultations.json")

# Lists and variables / queues
hide_markup = telebot.types.ReplyKeyboardRemove()
schedule_user_type = {}
schedule_user_day = {}
consult_user_type = {}
last_changes_id = ["0", "0"]
queue = {"new_last_changes_ten": [], "new_last_changes_eleven": [], "lastch_type": [],
         "lastch_settype": [], "schedule_type": [], "schedule_day": [], "schedule_group": [],
         "newadmin": [], "newmoder": [], "sendall": [], "consult_type": [], "consult_name": []}

         
# ALL THE MARKUPS:
start_markup = telebot.types.ReplyKeyboardMarkup(True, False)
start_markup.row('Расписание')
start_markup.row('Консультации')
start_markup.row('Контакты')

classes_markup = telebot.types.ReplyKeyboardMarkup(True, True)
classes_markup.row('10', '11')
classes_markup.row('Отмена')

weektype_markup = telebot.types.ReplyKeyboardMarkup(True, True)
weektype_markup.row('Числитель', 'Знаменатель')
weektype_markup.row('Последние изменения')
weektype_markup.row('Отмена')

canceling_markup = telebot.types.ReplyKeyboardMarkup(True, True)
canceling_markup.row('Отмена')
# END OF MARKUPS
         
         
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


def cancel_queue(message: dict):
    for item in queue:
        if {"id": message.from_user.id} in queue[item]:
            queue[item].remove({"id": message.from_user.id})
            print("REMOVED FROM {0} queue".format(item))
    print("QUEUES CANCELED")
        
        
# First handle all commands available and show the menu
@bot.message_handler(commands=['start'])
def handle_start(message):
    if not usermgr.issub(users_data, message.from_user.id):
        usermgr.adduser("subscribers", users_data, message.from_user.id)
        bot.send_sticker(message.from_user.id, constants.thumbup)
        bot.send_message(message.from_user.id, "Поздравляем! Теперь вы будете получать все новости!\n/unsub чтобы отписаться")
    bot.send_message(message.from_user.id, "Мы рады, что ты к нам присоединился!\nМеню создано.\nP.S. Начните вводить команду с '/', чтобы увидеть список команд",
                     reply_markup=start_markup)
    log(message, "Меню создано.")

@bot.message_handler(commands=['show'])
def handle_show(message):
    bot.send_message(message.from_user.id, "Меню создано.",
                     reply_markup=start_markup)
    log(message, "Меню создано.")
    
@bot.message_handler(commands=['hide'])
def handle_stop(message):
    bot.send_message(message.from_user.id, "Меню убрано.", reply_markup=hide_markup)
    log(message, "Меню убрано.")

    
@bot.message_handler(commands=['sendall'])
def handle_sendall(message):
    if usermgr.isadmin(users_data, message.from_user.id) or usermgr.ismoder(users_data, message.from_user.id):
        if not {"id": message.from_user.id} in queue['sendall']:
            queue['sendall'].append({"id": message.from_user.id})
        bot.send_message(message.from_user.id, "Что же мы всем отправим?", reply_markup=canceling_markup)
    else:
        answer = "У вас недостаточно прав для выполнения этой команды"
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
        
@bot.message_handler(func=lambda message: {"id": message.from_user.id} in queue['sendall'], content_types=['text', 'photo', 'sticker', 'audio', 'voice'])
def handle_sendall_forward(message):
    if (message.text == "Отмена"):
        cancel_queue(message)
        answer = "Отмена, возвращение в главное меню"
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
        log(message, answer)
        return
    mid = message.message_id
    queue['sendall'].remove({"id": message.from_user.id})
    for sub in usermgr.get_subs(users_data):
        bot.forward_message(sub['id'], message.from_user.id, mid)        
    
@bot.message_handler(commands=['sub'])
def handle_sub(message):
    if not usermgr.issub(users_data, message.from_user.id):
        usermgr.adduser("subscribers", users_data, message.from_user.id)
        bot.send_sticker(message.from_user.id, constants.thumbup)
        bot.send_message(message.from_user.id, "Поздравляем! Теперь вы будете получать все новости!\n/unsub чтобы отписаться")
    else:
        bot.send_sticker(message.from_user.id, constants.hugs)
        bot.send_message(message.from_user.id, "Вы уже подписаны на новости! :)\nМы рады, что вы цените наш труд.")

@bot.message_handler(commands=['unsub'])
def handle_unsub(message):
    if usermgr.issub(users_data, message.from_user.id):
        usermgr.removeuser("subscribers", users_data, message.from_user.id)
        bot.send_sticker(message.from_user.id, constants.armsin)
        bot.send_message(message.from_user.id, """Сожалеем, что вы приняли такое решение!
Мы будем благодарны, если вы расскажете, что вам не понравилось.
Напишите нам: beluckydaf@gmail.com""")
        bot.send_contact(message.from_user.id, "+79129992548", "Vladislav", "Smirnov")
    
    
@bot.message_handler(commands=['newadmin'])
def handle_newadmin(message):
    if usermgr.isadmin(users_data, message.from_user.id):
        queue["newadmin"].append(message.from_user.id)
        if message.from_user.id in queue["newmoder"]:
            queue["newmoder"].remove(message.from_user.id)
        answer = "Отправь контакт нового админа: "
        bot.send_message(message.from_user.id, answer, reply_markup=canceling_markup)
    else:
        answer = "У вас недостаточно прав для выполнения этой команды"
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)


@bot.message_handler(commands=['newmoder'])
def handle_newmoder(message):
    if usermgr.isadmin(users_data, message.from_user.id):
        queue["newmoder"].append(message.from_user.id)
        if message.from_user.id in queue["newadmin"]:
            queue["newadmin"].remove(message.from_user.id)
        answer = "Отправь контакт нового модератора: "
        bot.send_message(message.from_user.id, answer, reply_markup=canceling_markup)
    else:
        answer = "У вас недостаточно прав для выполнения этой команды"
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
    log(message, answer)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if not message.contact.user_id:
        if message.from_user.id in queue["newadmin"]:
            queue["newadmin"].remove(message.from_user.id)
        elif message.from_user.id in queue["newmoder"]:
            queue["newmoder"].remove(message.from_user.id)
        bot.send_message(message.from_user.id, "Увы, этого человека нет в Telegram.")
    if message.from_user.id in queue["newadmin"]:
        queue["newadmin"].remove(message.from_user.id)
        usermgr.adduser("admins", users_data, message.contact.user_id)
        bot.send_message(message.from_user.id, "Готово!")
        bot.send_message(message.contact.user_id, answers.admin_greeting)
        bot.send_message(message.contact.user_id, answers.great_resp)
    elif message.from_user.id in queue["newmoder"]:
        queue["newmoder"].remove(message.from_user.id)
        usermgr.adduser("moderators", users_data, message.contact.user_id) 
        bot.send_message(message.from_user.id, "Готово!")
        bot.send_message(message.contact.user_id, answers.moderator_greeting)
        bot.send_message(message.contact.user_id, answers.great_resp)


@bot.message_handler(commands=['setlast'])
def handle_setlast(message):
    if usermgr.isadmin(users_data, message.from_user.id):
        queue["lastch_settype"].append({"id": message.from_user.id})
        answer = "Выбери группу:"
        bot.send_message(message.from_user.id, answer, reply_markup=classes_markup)
    else:
        answer = """Только админ и его приближённые способны на такое!
Забудь, что написал, смертный! Я тоже притворюсь, будто не видел.
Согласен? Вот и отлично!
...Хееееей! Чем могу помочь?"""
        bot.send_message(message.from_user.id, answer)
    log(message, answer)


@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.from_user.id, answers.aboutme)
    log(message, answers.aboutme)


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
        for sub in usermgr.get_subs(users_data):
            bot.send_message(sub['id'], "Последние изменения для 10 классов обновлены!", reply_markup=start_markup)
        log(message, answer)
    elif {"id": message.from_user.id} in queue["new_last_changes_eleven"]:
        queue["new_last_changes_eleven"].remove({"id": message.from_user.id})
        last_changes_id[1] = str(message.photo[-1].file_id)
        answer = "Принял файл! Последние изменения обновлены!"
        bot.send_message(message.from_user.id, answer)
        for sub in usermgr.get_subs(users_data):
            bot.send_message(sub['id'], "Последние изменения для 11 классов обновлены!", reply_markup=start_markup)
        log(message, answer)


# Then texts ( keep collapsed unless you love pain )
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_text(message):
    answer = ""
    if (message.text == "Отмена"):
        cancel_queue(message)
        answer = "Отмена, возвращение в главное меню"
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
    elif {"id": message.from_user.id} in queue["lastch_settype"]:
        queue["lastch_settype"].remove({"id": message.from_user.id})
        if (message.text == "10"):
            queue["new_last_changes_ten"].append({"id": message.from_user.id})
            answer = "Загружай:"
            bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
        elif (message.text == "11"):
            queue["new_last_changes_eleven"].append({"id": message.from_user.id})
            answer = "Загружай:"
            bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
        else:
            answer = "Лол..."
            bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
    elif {"id":message.from_user.id} in queue["lastch_type"]:
        queue["lastch_type"].remove({"id":message.from_user.id})
        if (message.text == "10"):
            if last_changes_id[0] == "0":
                    answer = "Я пока не знаю изменений..."
                    bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
            else:
                    bot.send_chat_action(message.from_user.id, 'upload_photo')
                    bot.send_photo(message.from_user.id, last_changes_id[0], reply_markup=start_markup)
                    answer = "Попытались отправить фото, надеемся, получилось."
        elif (message.text == "11"):
            if last_changes_id[1] == "0":
                    answer = "Я пока не знаю изменений..."
                    bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
            else:
                    bot.send_chat_action(message.from_user.id, 'upload_photo')
                    bot.send_photo(message.from_user.id, last_changes_id[1], reply_markup=start_markup)
                    answer = "Попытались отправить фото, надеемся, получилось."
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
                user_markup.row("Отмена")
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
                user_markup.row("Отмена")
                bot.send_message(message.from_user.id, answers.schedule_day, reply_markup=user_markup)
                answer = answers.schedule_day + "\nДобавлен в лист ожидания ответа."
        else:
            answer = "НЕТ ТАКОГО ТИПА РАСПИСАНИЯ!"
            bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
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
            user_markup.row("Отмена")
            bot.send_message(message.from_user.id, answers.schedule_group, reply_markup=user_markup)
            answer = answers.schedule_group + "\nДобавлен в лист ожидания ответа."
        else:
            answer = "НЕТ ТАКОГО ДНЯ НЕДЕЛИ!"
            bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
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
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
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
        bot.send_message(message.from_user.id, answers.schedule_type, reply_markup=weektype_markup)
        answer = answers.schedule_type + "\nДобавлен в лист ожидания ответа."
    elif message.text == "Контакты":
        bot.send_message(message.from_user.id, answers.contacts)
        answer = answers.contacts
    elif message.text == "Консультации":
        queue["consult_type"].append({"id": message.from_user.id})
        data = cnslt_data.getcontents()
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        for i in data:
            user_markup.row(i)
        user_markup.row('Отмена')
        answer = "Выбери предмет:"
        bot.send_message(message.from_user.id, answer, reply_markup=user_markup)
    elif {"id": message.from_user.id} in queue["consult_type"]:
        queue["consult_type"].remove({"id": message.from_user.id})
        data = cnslt_data.getcontents()
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        if message.text in data:
            consult_user_type[message.from_user.id] = message.text
            for i in data[message.text]:
                user_markup.row(i["name"])
            user_markup.row('Отмена')
            queue["consult_name"].append({"id": message.from_user.id})
            answer = "Выбери преподавателя:"
            bot.send_message(message.from_user.id, answer, reply_markup=user_markup)
        else:
            answer = "Нет такого предмета:"
            bot.send_message(message.from_user.id, answer, reply_markup=user_markup)
    elif {"id": message.from_user.id} in queue["consult_name"]:
        queue["consult_name"].remove({"id": message.from_user.id})
        data = cnslt_data.getcontents()
        type = consult_user_type.pop(message.from_user.id)
        boo = False
        for i in data[type]:
            if i["name"] == message.text:
                boo = True
                answer = "Предмет: {0}\nПреподаватель: {1}\nАудитория: {2}\nДни: {3}".format(type, i["name"], i["room"], i["time"])
        if boo == False:
            answer = "Нет такого преподавателя"
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
            
    else:
        answer = answers.cant_understand
        bot.send_message(message.from_user.id, answer, reply_markup=start_markup)
    
    log(message, answer)

# Remove webhook, it fails sometimes to set if there is a previous webhook
# Do not comment this line. If there's a webhook set, regular polling won't work
bot.remove_webhook()

# Legacy ( for debugging on a local machine )
# bot.polling(none_stop=True, interval=0)

# Set webhook ( comment the following 2 lines if debugging )
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

# Comment the following line when debugging
cherrypy.quickstart(WebhookServer(), constants.WEBHOOK_URL_PATH, {'/': {}})

