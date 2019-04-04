#!usr/bin/env python3
from getch import getch
from termcolor import colored
from userinput import UserInput
import os


def main():
    s = UserInput('Hello world, huy!')
    os.system('clear')
    print(s.text)
    while not (s.is_done()):
        key = getch()
        s.update(key)
        os.system('clear')
        print('{}{}{}'.format(colored(s.correct_text(), 'green'),
                              colored(s.get_incorrect_symbol(), 'red'),
                              s.get_black_text()))
        print('{}{}'.format(colored(s.correct_input, 'green'),
                            colored(s.incorrect_text, 'red')))
    os.system('clear')
    print(colored(s.text, 'green'))
    print('Accurate: {:.2%}'.format(s.accurate))


if __name__ == '__main__':
    main()
