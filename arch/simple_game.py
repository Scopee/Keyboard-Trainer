import sys
import time
import timeit
from threading import Thread

from termcolor import colored

from arch.game import Game
from arch.texts_storage import TextStorage


class SimpleGame(Game):
    def __init__(self, label, dir_name=""):
        self.text_storage = TextStorage(dir_name)
        self.text_name, text = self.text_storage.get_random_string(label)
        super().__init__(text)
        self.printing_thread = Thread(target=self.print_thread)
        self.inp_thread = Thread(target=self.input_thread)

    def start_game(self):
        self.set_timer(self.current_state_string(self.user_input))
        self._start_time = timeit.default_timer()
        self.inp_thread.start()
        self.printing_thread.start()
        self.inp_thread.join()
        self.printing_thread.join()
        if self.is_exit:
            self.clear()
            sys.exit()
        res_time = timeit.default_timer() - self._start_time
        if self.is_finished:
            self.print_results(self.result_string(self.user_input, res_time))
            self.get_label(self.text_storage, self.text_name)
        self._user.update_stat(self.user_input, res_time,
                               self.calc_current_speed())

    def calc_current_speed(self):
        count = self.user_input.count
        curr_time = timeit.default_timer()
        res_time = (curr_time - self._start_time) / 60
        return int(count // res_time)

    def result_string(self, user_input, res_time):
        self.clear()
        s = f'{colored(user_input.text, "green")}\r\n' \
            f'{self._strings["acc"]}:{user_input.accurate:.2%}' \
            f'\r\n\r{self._strings["time"]}:' \
            f'{res_time:.2f} {self._strings["sec"]}\r\n' \
            f'{self._strings["avg_speed"]}: ' \
            f'{self.calc_current_speed()} ' \
            f'{self._strings["speed"]}' \
            f'\r\n\r{self._strings["err"]}: {user_input.error_count}'
        return s

    def current_state_string(self, user_input):
        s = f'{colored(user_input.correct_text(), "green")}' \
            f'{colored(user_input.get_incorrect_symbol(), "red")}' \
            f'{user_input.get_blank_text()}\r\n' \
            f'{colored(user_input.correct_input, "green")}' \
            f'{colored(user_input.incorrect_text, "red")}\r\n' \
            f'{self._strings["cur_speed"]}: ' \
            f'{self.calc_current_speed()}' \
            f' { self._strings["speed"]}\r\n' \
            f'{self._strings["err"]}: {self.user_input.error_count}\r'
        return s

    def print_thread(self):
        while not self.user_input.is_done():
            if not self.inp_thread.is_alive():
                break
            self.print_results(self.current_state_string(self.user_input))
            time.sleep(0.5)

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
