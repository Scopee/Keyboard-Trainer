#!/usr/bin/env python3
import argparse

import arch.generator as gen
import arch.settings as settings
from arch.menu import Menu


def main(dir_name):
    gen.check_texts(dir_name)
    menu = Menu(dir_name)
    menu.run()


def print_help():
    sett = settings.load_from_settings()
    strings = sett['STRINGS.{}'.format(sett['USER']['language'])]
    print(strings['about'])
    print(strings['help'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Keyboard Trainer")
    parser.add_argument('-d', type=str, default="", help="Directory to texts.")
    args = parser.parse_args()
    main(args.d)
