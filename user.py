import configparser
import os.path

STRINGS = {
    'ru': {
        'welcome': 'Добро пожаловать',
        'select': 'Выберите режим',
        'start': 'Начать игру',
        'exit': 'Выход',
        'acc': 'Точность',
        'time': 'Время',
        'sec': 'сек',
        'press': 'Нажмите Enter для продолжения',
        'settings': 'Настройки',
        'language': 'Язык',
        'username': 'Никнейм',
        'select_menu': 'Выберите'
    },
    'en': {
        'welcome': 'Welcome',
        'select': 'Select option',
        'start': 'Start game',
        'exit': 'Exit',
        'acc': 'Accurate',
        'time': 'Time',
        'sec': 'sec',
        'press': 'Press Enter to continue',
        'settings': 'Settings',
        'language': 'Language',
        'username': 'Nickname',
        'select_menu': 'Select'
    }
}


class User:
    def __init__(self):
        self._nick = ''
        self._language = ''
        self.update_config()

    @property
    def name(self):
        return self._nick

    @staticmethod
    def load_from_settings():
        if not os.path.exists('settings.ini'):
            config = configparser.ConfigParser()
            config['USER'] = {'username': 'User', 'language': 'en'}
            with open('settings.ini', 'w') as f:
                config.write(f)
        config = configparser.ConfigParser()
        config.read('settings.ini')
        return config['USER']

    def get_strings(self):
        return STRINGS[self._language]

    def update_config(self):
        setting = self.load_from_settings()
        self._nick = setting['username']
        self._language = setting['language']
