from getch import Getch
from game import Game
from user import User
import configparser
import os


class Menu:
    def __init__(self):
        self._settings_menu = {}
        self._menu_items = {}
        self._user = User()
        self._strings = self._user.get_strings()
        self._getch = Getch()

    def run(self):
        while True:
            self.print_options()
            option = self._getch()
            if option == '1':
                self.start_game()
            elif option in {'2', '\x03'}:
                os.system('clear')
                break

    def print_options(self):
        os.system('clear')
        print('{}, {}'.format(self._strings['welcome'], self._user.name))
        print(self._strings['select'])
        print()
        for k, v in self._menu_items.items():
            print('{}. {}'.format(k, v))

    def start_game(self):
        game = Game()
        game.start_game()
        print('{}'.format(self._user.get_strings()['press']))
        while self._getch() != '\r':
            pass
