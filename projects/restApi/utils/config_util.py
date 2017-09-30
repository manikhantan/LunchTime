import os
import configparser

from projects import API_DIR

config = None


def get_config():
    global config
    if not config:
        config = configparser.ConfigParser()
        config_path = os.path.join(API_DIR, 'conf.ini')
        config.read(config_path)
    return config
