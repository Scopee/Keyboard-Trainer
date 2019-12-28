import os
import configparser
from arch.user import User

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_from_settings():
    if not os.path.exists(f'{PATH}/settings.ini'):
        config = configparser.ConfigParser()
        config['USER'] = {'username': 'User', 'language': 'EN'}
        write_settings(config)
    config = configparser.ConfigParser()
    config.read(f'{PATH}/settings.ini')
    return config


def change_user(new_user):
    config = load_from_settings()
    config['USER']['username'] = new_user
    write_settings(config)
    users = User.load_users()
    stats = User.load_full_stat(new_user)
    user = User(new_user)
    if new_user not in users:
        stats[new_user] = user.load_statistics()
        User.write_statistics(stats)
    write_settings(config)


def get_name_from_config():
    setting = load_from_settings()
    return setting['USER']['username']


def write_settings(config):
    with open(f'{PATH}/settings.ini', 'w') as f:
        config.write(f)
