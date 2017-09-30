import sys
import requests
from time import gmtime, strftime
import os
path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(path)
sys.path.append(path)

from projects.restApi.utils.config_util import get_config
from projects.restApi.utils.redis_util import get_connection


def get_time_key():
    return strftime("%H-%M", gmtime())


def send_message(message):
    configs = get_config()
    webhook_url = configs['API_TOKENS']['WEBHOOK_URL']
    message = {'text': message}
    r = requests.post(webhook_url, json=message)
    return


def send_messages():
    conn = get_connection()
    time_key = get_time_key()
    msg = conn.get(time_key)
    if msg:
        send_message(msg.decode('ascii'))


if __name__ == '__main__':
    send_messages()
