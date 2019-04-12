import os
import configparser


class Settings:
    @staticmethod
    def load_from_settings():
        if not os.path.exists('settings.ini'):
            config = configparser.ConfigParser()
            config['USER'] = {'username': 'User', 'language': 'en'}
            with open('settings.ini', 'w') as f:
                config.write(f)
        config = configparser.ConfigParser()
        config.read('settings.ini')
        return config
