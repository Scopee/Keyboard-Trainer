from arch.userinput import UserInput
import os
from termcolor import colored
import timeit
from arch.getch import Getch
from arch.user import User


class Game:
    def __init__(self):
        text = 'Спустя неделю после рождения нашей дочери Лорен мы'
        self._user = User()
        self._user_input = UserInput(text)
        self._getch = Getch()

    def start_game(self):
        os.system('clear')
        print(self._user_input.text)
        start_time = timeit.default_timer()
        is_finished = True
        while not (self._user_input.is_done()):
            key = self._getch()
            if key == '\x1b':
                is_finished = False
                break
            self._user_input.update(key)
            os.system('clear')
            print('{}{}{}'.format(
                colored(self._user_input.correct_text(), 'green'),
                colored(self._user_input.get_incorrect_symbol(),
                        'red'),
                self._user_input.get_blank_text()))
            print(
                '{}{}'.format(colored(self._user_input.correct_input, 'green'),
                              colored(self._user_input.incorrect_text, 'red')))
        time = timeit.default_timer()
        if is_finished:
            os.system('clear')
            print(colored(self._user_input.text, 'green'))
            print('{}: {:.2%}'.format(self._user.get_strings()['acc'],
                                      self._user_input.accurate))
            print('{}: {:.2f} {}'.format(self._user.get_strings()['time'],
                                         time - start_time,
                                         self._user.get_strings()['sec']))
