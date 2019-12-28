import arch.settings as settings
from datetime import datetime
import json


class User:
    def __init__(self, nick):
        self._nick = nick
        self._language = ''
        self._strings = {}
        self.stat = {}
        self.update_config()
        self.stat = self.load_statistics()

    @property
    def name(self):
        return self._nick

    def get_strings(self):
        return self._strings

    def update_config(self):
        setting = settings.load_from_settings()
        self._nick = setting['USER']['username']
        self._language = setting['USER']['language']
        self._strings = setting['STRINGS.' + self._language]

    def update_stat(self, user_input, res_time, speed):
        self.load_statistics()
        self.stat['text_count'] += 1
        self.stat['symbol_count'] += user_input.count
        self.stat['all_time'] += res_time / 60
        self.stat['errors'] += user_input.error_count
        self.stat['average_speed'] = self.stat['symbol_count'] // self.stat[
            'all_time']
        self.stat['average_errors'] \
            = self.stat['errors'] // self.stat['text_count']
        self.stat['max_speed'] = speed \
            if speed > self.stat['max_speed'] else self.stat['max_speed']
        dynamic = self.stat['dynamic']
        date = datetime.now().strftime('%B/%y')
        if date not in dynamic:
            dynamic[date] = {}
            dynamic[date]['text_count'] = 1
            dynamic[date]['symbol_count'] = user_input.count
            dynamic[date]['all_time'] = res_time / 60
            dynamic[date]['average_speed'] = int(
                dynamic[date]['symbol_count'] / dynamic[date]['all_time'])
        else:
            dynamic[date]['text_count'] += 1
            dynamic[date]['symbol_count'] += user_input.count
            dynamic[date]['all_time'] += res_time / 60
            dynamic[date]['average_speed'] = int(
                dynamic[date]['symbol_count'] / dynamic[date]['all_time'])
        self.stat['dynamic'] = dynamic
        self.update_user_state(self.stat)

    @staticmethod
    def load_full_stat(username):
        try:
            with open(f'{settings.PATH}/statistics.json') as f:
                stat = json.load(f)
                return stat
        except FileNotFoundError:
            return {username: {'text_count': 0,
                               'symbol_count': 0,
                               'all_time': 0,
                               'average_speed': 0,
                               'max_speed': 0,
                               'errors': 0,
                               'average_errors': 0,
                               'dynamic': {}}}

    def get_stat(self):
        self.stat = self.load_statistics()
        return self.stat

    def load_statistics(self):
        stat = User.load_full_stat(self._nick)
        if self._nick in stat.keys():
            stat = stat[self._nick]
        else:
            stat = {
                'text_count': 0,
                'symbol_count': 0,
                'all_time': 0,
                'average_speed': 0,
                'max_speed': 0,
                'errors': 0,
                'average_errors': 0,
                'dynamic': {}
            }
        return stat

    @staticmethod
    def load_users():
        try:
            with open(f'{settings.PATH}/statistics.json') as f:
                return json.load(f).keys()
        except FileNotFoundError:
            return []

    @staticmethod
    def write_statistics(data):
        with open(f'{settings.PATH}/statistics.json', 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False))

    def update_user_state(self, user_data):
        stats = User.load_full_stat(self._nick)
        stats[self._nick] = user_data
        User.write_statistics(stats)
