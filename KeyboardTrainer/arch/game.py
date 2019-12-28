import os
import sys
import time
import timeit

import arch.getch as getch
import arch.settings as settings
from arch.user import User
from arch.userinput import UserInput


class Game:
    TIMER = 5

    def __init__(self, text):
        self._user = User(settings.get_name_from_config())
        self._strings = self._user.get_strings()
        self._start_time = 0
        self._res_time = 0
        self.user_input = UserInput(text)
        self.is_finished = True
        self.is_exit = False

    def get_user_input(self):
        key = getch.getch()
        if key == '\x1b':
            return None
        return key

    def calc_current_speed(self):
        count = self.user_input.count
        curr_time = timeit.default_timer()
        res_time = (curr_time - self._start_time) / 60
        return int(count // res_time)

    def set_timer(self, state):
        try:
            for i in range(self.TIMER, -1, -1):
                self.print_results(state)
                if i == 0:
                    print('Start')
                    continue
                print(i)
                time.sleep(1)
        except KeyboardInterrupt:
            Game.clear()
            sys.exit()

    def get_label(self, text_storage, text_name):
        print(self._strings['label'])
        print(f"1. {self._strings['yes']}")
        print(f"2. {self._strings['no']}")
        choice = getch.getch()
        label = None
        if choice == "1":
            label = input(self._strings['write_label'])

        if label is not None:
            text_storage.add_label(text_name, label)

    def print_results(self, results):
        self.clear()
        print(results)

    @staticmethod
    def clear():
        os.system('echo -e \\\\033c')
        # os.system('clear')
