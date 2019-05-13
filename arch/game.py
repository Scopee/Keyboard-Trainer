import os
import sys
import time
import timeit
from threading import Thread

from termcolor import colored

from arch.generator import Generator
from arch.getch import Getch
from arch.user import User
from arch.userinput import UserInput


class Game:
    def __init__(self):
        gen = Generator()
        text = gen.get_random_string()
        self._user = User()
        self.user_input = UserInput(text)
        self._getch = Getch()
        self._start_time = 0
        self.printing_thread = Thread(target=self.print_thread)
        self.inp_thread = Thread(target=self.input_thread)
        self.is_finished = True
        self.is_exit = False

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')
        # os.system('clear')

    def start_game(self):
        self.set_timer()
        self._start_time = timeit.default_timer()
        self.printing_thread.start()
        self.inp_thread.start()
        self.printing_thread.join()
        self.inp_thread.join()
        if self.is_exit:
            self.clear()
            sys.exit()
        res_time = timeit.default_timer()
        if self.is_finished:
            self.print_results(self.result_string(self.user_input,
                                                  res_time - self._start_time))

    def get_user_input(self):
        key = self._getch()
        if key == '\x1b':
            return None
        return key

    def calc_current_speed(self):
        count = self.user_input.count
        curr_time = timeit.default_timer()
        res_time = (curr_time - self._start_time) / 60
        return int(count // res_time)

    def print_results(self, results):
        self.clear()
        print(results)

    def result_string(self, user_input, res_time):
        self.clear()
        return '{}\n\r{}: {:.2%}\n\r{}: {:.2f} {}\n\r{}: {} {}\n\r{}: {}' \
            .format(
                colored(user_input.text, 'green'),
                self._user.get_strings()['acc'],
                user_input.accurate,
                self._user.get_strings()['time'],
                res_time,
                self._user.get_strings()['sec'],
                self._user.get_strings()['avg_speed'],
                self.calc_current_speed(),
                self._user.get_strings()['speed'],
                self._user.get_strings()['err'],
                user_input.error_count,
            )

    def current_state_string(self, user_input):
        return '{}{}{}\r\n{}{}\r\n{}: {} {}\r\n{}: {}\r\n'.format(
            colored(user_input.correct_text(), 'green'),
            colored(user_input.get_incorrect_symbol(), 'red'),
            user_input.get_blank_text(),
            colored(user_input.correct_input, 'green'),
            colored(user_input.incorrect_text, 'red'),
            self._user.get_strings()['cur_speed'],
            self.calc_current_speed(),
            self._user.get_strings()['speed'],
            self._user.get_strings()['err'],
            self.user_input.error_count
        )

    def set_timer(self):
        try:
            for i in range(5, -1, -1):
                self.print_results(self.current_state_string(self.user_input))
                if i == 0:
                    print('Start')
                    continue
                print(i)
                time.sleep(1)
        except KeyboardInterrupt:
            self.clear()
            sys.exit()

    def print_thread(self):
        while not self.user_input.is_done():
            if not self.inp_thread.is_alive():
                break
            self.print_results(self.current_state_string(self.user_input))
            time.sleep(1)

    def input_thread(self):
        while not self.user_input.is_done():
            symbol = self.get_user_input()
            if symbol == '\x03':
                self.is_exit = True
                break
            if symbol is None:
                self.is_finished = False
                break
            self.user_input.update(symbol)
            self.print_results(self.current_state_string(self.user_input))
