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

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

# CHERRYPY CONSTANTS
WEBHOOK_HOST = "188.166.82.60"
WEBHOOK_PORT = 88
WEBHOOK_LISTEN = "0.0.0.0"

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % token
# END OF CHERRYPY

# STICKERS IDS
thumbup = "BQADAgADGQADyIsGAAFl6KYZBflVyQI"
hugs = "BQADAgADPgADyIsGAAEuCrQ7AXgedwI"
armsin = "BQADAgADIwADyIsGAAHeuQrNOU12cgI"
# END OF STICKERS