from pathlib import Path
from babel import Locale


cwd = Path().cwd()

TOKEN = '5413876625:AAGKrFYdPfW_Je0QGud2z6wk3u0TO_mZPfQ'

ADMINS = [444083371, 999678965]


WEBHOOK_HOST = 'https://142.93.230.250'
WEBHOOK_PATH = f'{cwd.name}'
WEBHOOK_URL = f"{WEBHOOK_HOST}/{WEBHOOK_PATH}/"

BOT_SERVER = {
    'host': '127.0.0.1',
    'port': 2000
}


REDIS = {
    'db': 2,
    'prefix': cwd.name
}


MYSQL = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'db': 'manicure_report_db',
    # 'unix_socket': '/var/run/mysqld/mysqld.sock'
}
