from arch.userinput import UserInput
from termcolor import colored
from arch.getch import Getch
from arch.user import User
from arch.generator import Generator
import time
import timeit
import os


class Game:
    def __init__(self):
        gen = Generator()
        text = gen.get_random_string()
        self._user = User()
        self._user_input = UserInput(text)
        self._getch = Getch()
        self._start_time = 0

    @staticmethod
    def clear():
        """
        Clears the terminal screen and scroll back to present
        the user with a nice clean, new screen. Useful for managing
        menu screens in terminal applications.
        """
        os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')

    def start_game(self):
        self.set_timer()
        self._start_time = timeit.default_timer()
        is_finished = True
        while not self._user_input.is_done():
            symbol = self.get_user_input()
            if symbol is None:
                is_finished = False
                break
            self._user_input.update(symbol)
            self.print_current_state(self._user_input)
        res_time = timeit.default_timer()
        if is_finished:
            self.print_result(self._user_input, res_time - self._start_time)

    def get_user_input(self):
        key = self._getch()
        if key == '\x1b':
            return None
        if key == '\x03':
            self.clear()
            exit()
        return key

    def calc_current_speed(self):
        count = self._user_input.count
        curr_time = timeit.default_timer()
        res_time = (curr_time - self._start_time) / 60
        return int(count // res_time)

    def print_current_state(self, user_input):
        self.clear()
        print('{}{}{}'.format(
            colored(user_input.correct_text(), 'green'),
            colored(user_input.get_incorrect_symbol(), 'red'),
            user_input.get_blank_text()))
        print(
            '{}{}'.format(colored(user_input.correct_input, 'green'),
                          colored(user_input.incorrect_text, 'red')))
        print('{}: {} {}'.format(self._user.get_strings()['cur_speed'],
                                 self.calc_current_speed(),
                                 self._user.get_strings()['speed']))
        print('{}: {}'.format(self._user.get_strings()['err'],
                              self._user_input.error_count))

    def print_result(self, user_input, res_time):
        self.clear()
        print(colored(user_input.text, 'green'))
        print('{}: {:.2%}'.format(self._user.get_strings()['acc'],
                                  user_input.accurate))
        print('{}: {:.2f} {}'.format(self._user.get_strings()['time'],
                                     res_time,
                                     self._user.get_strings()['sec']))
        print('{}: {}'.format(self._user.get_strings()['avg_speed'],
                              self.calc_current_speed()))
        print('{}: {}'.format(self._user.get_strings()['err'],
                              user_input.error_count))

    def set_timer(self):
        for i in range(5, -1, -1):
            self.print_current_state(self._user_input)
            if i == 0:
                print('Start')
                continue
            print(i)
            time.sleep(1)
