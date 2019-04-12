from arch.settings import Settings


class User:
    def __init__(self):
        self._nick = ''
        self._language = ''
        self._strings = {}
        self.update_config()

    @property
    def name(self):
        return self._nick

    def get_strings(self):
        return self._strings

    def update_config(self):
        setting = Settings.load_from_settings()
        self._nick = setting['USER']['username']
        self._language = setting['USER']['language']
        self._strings = setting['STRINGS.' + self._language]
