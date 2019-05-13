from arch.getch import Getch
from arch.game import Game
from arch.user import User
import os


class Menu:
    def __init__(self):
        self._user = User()
        self._strings = self._user.get_strings()
        self._menu_items = {
            '1': self._strings['start'],
            '2': self._strings['exit']
        }
        self._getch = Getch()

    def run(self):
        while True:
            self.print_options()
            option = self._getch()
            if option == '1':
                self.start_game()
            elif option in {'2', '\x03'}:
                Game.clear()
                break

    def print_options(self):
        # os.system('clear')
        Game.clear()
        strings = self._user.get_strings()
        print('{}, {}'.format(strings['welcome'], self._user.name))
        print(strings['select'])
        print()
        for k, v in self._menu_items.items():
            print('{}. {}'.format(k, v))

    def start_game(self):
        game = Game()
        game.start_game()
        print('{}'.format(self._user.get_strings()['press']))
        while self._getch() != '\r':
            pass
