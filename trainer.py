#!/usr/local/bin/python3
from arch.menu import Menu
from arch.generator import Generator
from arch.settings import Settings
import sys


def main():
    Generator.check_texts()
    args = sys.argv
    if len(args) > 1:
        print_help()
    else:
        menu = Menu()
        menu.run()


def print_help():
    settings = Settings.load_from_settings()
    lang = settings['USER']['language']
    strings = settings['STRINGS.' + lang]
    print(strings['about'])
    print(strings['help'])


if __name__ == '__main__':
    main()
