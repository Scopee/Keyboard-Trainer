import os
import sys
import time
import timeit
from threading import Thread

from termcolor import colored

from arch.game import Game
from arch.simple_game import SimpleGame
from arch.texts_storage import TextStorage
from arch.userinput import UserInput


class EnemyGame(Game):
    TIMER = 5

    def __init__(self, enemy_speed, label, dir_name=""):
        self.text_storage = TextStorage(dir_name)
        self.text_name, text = self.text_storage.get_random_string(label)
        super().__init__(text)
        self.enemy_input = UserInput(text)
        self.enemy_speed = enemy_speed
        self.inp_thread = Thread(target=self.input_thread)
        self.en_thread = Thread(target=self.enemy_thread)
        self.upd_thread = Thread(target=self.print_thread)
        self.threads_active = False
        self.enemy_finish = None

    def start_game(self):
        self.set_timer(self.current_state
                       (self.current_enemy_state(self.enemy_input),
                        self.current_state_string(self.user_input)))
        self._start_time = timeit.default_timer()
        self.inp_thread.start()
        self.en_thread.start()
        self.threads_active = True
        self.inp_thread.join()
        self.en_thread.join()
        if self.is_exit:
            SimpleGame.clear()
            sys.exit()
        finish_time = timeit.default_timer()
        res_time = finish_time - self._start_time
        if self.is_finished:
            self.print_results(self.current_state(None,
                                                  self.result_string(
                                                      self.user_input,
                                                      res_time,
                                                      finish_time)))
            self.get_label(self.text_storage, self.text_name)
        self._user.update_stat(self.user_input, res_time,
                               self.calc_current_speed())

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
            self.print_results(
                self.current_state(self.current_enemy_state(self.enemy_input),
                                   self.current_state_string(self.user_input)))

    def print_thread(self):
        while not self.user_input.is_done():
            if not self.inp_thread.is_alive():
                break
            self.print_results(
                self.current_state(self.current_enemy_state(self.enemy_input),
                                   self.current_state_string(self.user_input)))
            time.sleep(0.5)

    def enemy_thread(self):
        while not self.enemy_input.is_done():
            if not self.inp_thread.is_alive():
                break
            symbol = self.enemy_input.get_blank_text()[0]
            self.enemy_input.update(symbol)
            spd = (self.enemy_speed // 60) or 1
            time.sleep(1 / spd)
            self.print_results(
                self.current_state(self.current_enemy_state(self.enemy_input),
                                   self.current_state_string(self.user_input)))
        self.enemy_finish = timeit.default_timer()
        self.upd_thread.start()
        self.upd_thread.join()

    def result_string(self, user_input, res_time, finish_time):
        s = f'{colored(user_input.text, "green")}\r\n' \
            f'{self._strings["acc"]}: ' \
            f'{user_input.accurate:.2%}\r\n' \
            f'{self._strings["time"]}: {res_time:.2f} ' \
            f'{self._strings["sec"]}\r\n' \
            f'{self._strings["avg_speed"]}:' \
            f' {self.calc_current_speed()} ' \
            f'{self._strings["speed"]}\r\n' \
            f'{self._strings["err"]}: ' \
            f'{user_input.error_count}\r\n' \
            f'{self._strings["delta"]}: ' \
            f'{finish_time - self.enemy_finish:.2f} ' \
            f'{self._strings["sec"]}'
        return s

    def current_state_string(self, user_input):
        s = f'{colored(user_input.correct_text(), "green")}' \
            f'{colored(user_input.get_incorrect_symbol(), "red")}' \
            f'{user_input.get_blank_text()}\r\n' \
            f'{colored(user_input.correct_input, "green")}' \
            f'{colored(user_input.incorrect_text, "red")}\r\n' \
            f'{self._strings["cur_speed"]}: ' \
            f'{self.calc_current_speed()} ' \
            f'{self._strings["speed"]}\r\n' \
            f'{self._strings["err"]}: ' \
            f'{self.user_input.error_count}\r'
        return s

    def current_state(self, enemy_res, user_res):
        res = user_res
        rows = os.get_terminal_size().columns
        if enemy_res:
            res = f"{enemy_res}\r\n{'-' * rows}\r\n{user_res}"
        return res

    def current_enemy_state(self, user_input):
        return '{}{}{}\r\n'.format(
            colored(user_input.correct_text(), 'magenta'),
            colored(user_input.get_incorrect_symbol(), 'red'),
            user_input.get_blank_text(),
        )
