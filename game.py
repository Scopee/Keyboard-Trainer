from userinput import UserInput
import os
from termcolor import colored
import timeit
from getch import Getch


class Game:
    def __init__(self):
        text = 'Спустя неделю после рождения нашей дочери Лорен мы ' \
               'с Бонни чувствовали себя совершенно измотанными. ' \
               'Ночами ребенок то и дело будил нас.'
        self._user_input = UserInput(text)
        self._getch = Getch()

    def start_game(self):
        os.system('clear')
        print(self._user_input.text)
        start_time = timeit.default_timer()
        while not (self._user_input.is_done()):
            key = self._getch()
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
        os.system('clear')
        print(colored(self._user_input.text, 'green'))
        print('Accurate: {:.2%}'.format(self._user_input.accurate))
        print('Time: {:.2f} seconds'.format(time - start_time))


