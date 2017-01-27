#!/usr/bin/python3

# Important
token = "316879287:AAGa7sj9yaO-3FjL55U97cNaKZaXTcIl6Dg"
schedule_path = "schedule{0}.json"
users_path = "users.json"
# Less important
schedule_types = ["Числитель", "Знаменатель", "Последние изменения"]
schedule_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
groups = ["101", "102", "103", "104", "111", "112", "113", "114"]
# admins = [146505982, 183562293]

WEBHOOK_HOST = '138.68.134.251'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)
