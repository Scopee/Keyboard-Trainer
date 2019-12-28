import os

import arch.getch as getch
import arch.settings as settings
from arch.enemy_game import EnemyGame
from arch.simple_game import SimpleGame
from arch.texts_storage import TextStorage
from arch.user import User


class Menu:
    def __init__(self, dir_name):
        self._user = User(settings.get_name_from_config())
        self._strings = self._user.get_strings()
        self._dir_name = dir_name
        self._text_st = TextStorage(dir_name)
        self._menu_items = {
            '1': self._strings['start'],
            '2': self._strings['enemy_game'],
            '3': self._strings['show_stat'],
            '4': self._strings['change_user'],
            '5': self._strings['exit']
        }

        self._actions = {
            "1": self.start_game,
            "2": self.start_enemy_game,
            "3": self.show_stat,
            '4': self.change_name,
            '5': SimpleGame.clear
        }

    def run(self):
        if not os.path.exists(f'{settings.PATH}/statistics.json'):
            self.change_name()
        while True:
            self.print_options()
            option = getch.getch()
            if option in self._actions:
                self._actions[option]()
            if option == "5":
                break
            self._user.load_statistics()

    def change_name(self):
        SimpleGame.clear()
        new_name = input(self._strings['input_name'] + ' ')
        settings.change_user(new_name)
        self._user.update_config()
        self._user = User(settings.get_name_from_config())

    def print_options(self):
        SimpleGame.clear()
        strings = self._user.get_strings()
        print(f'{strings["welcome"]}, {self._user.name}')
        print(strings['select'])
        print()
        for k, v in self._menu_items.items():
            print(f'{k}. {v}')

    def start_game(self):
        label = self.get_label()
        game = SimpleGame(label, self._dir_name)
        game.start_game()
        print(f'{self._user.get_strings()["press"]}')
        while getch.getch() != '\r':
            pass

    def start_enemy_game(self):
        label = self.get_label()
        speed = self._user.stat['max_speed']
        game = EnemyGame(speed + 5, label, self._dir_name)
        game.start_game()
        print(f'{self._user.get_strings()["press"]}')
        while getch.getch() != '\r':
            pass

    def get_label(self):
        print(self._strings['choose_label'])
        print(f"1. {self._strings['choose_label_yes']}")
        print(f"2. {self._strings['choose_label_no']}")
        choice = getch.getch()
        if choice == "1":
            print(self.get_all_labels())
            label = input(self._strings['write_label'])
            if label in self._text_st.get_all_labels():
                return label
            else:
                return None
        elif choice == "2":
            return None

    def get_all_labels(self):
        labels = self._text_st.get_all_labels()
        return '\n'.join(labels)

    def show_stat(self):
        SimpleGame.clear()
        stat = self._user.get_stat()
        res = f'{self._strings["user"]} {self._user.name}\n' \
            f'{self._strings["text_count"]}: {stat["text_count"]}\n' \
            f'{self._strings["symbol_count"]}: {stat["symbol_count"]}\n' \
            f'{self._strings["average_speed"]}: {stat["average_speed"]} ' \
            f'{self._strings["speed"]}\n' \
            f'{self._strings["average_errors"]}: {stat["average_errors"]}\n' \
            f'{self._strings["dynamics"]}:\n'

        dynamic = stat['dynamic']
        for k, v in dynamic.items():
            res += f'{k}: {v["average_speed"]} {self._strings["speed"]}\n'
        print(res)
        print(f'{self._user.get_strings()["press"]}')
        while getch.getch() != '\r':
            pass
