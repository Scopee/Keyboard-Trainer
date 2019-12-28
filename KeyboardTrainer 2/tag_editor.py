#!/usr/bin/env python3
import os
import json
import sys
import tty
import termios
import argparse


def main(path_to_file):
    actions = {
        '1': print_tags,
        '2': print_texts,
        '3': remove_tag_from_text,
        '4': remove_tag,
        '5': add_tag,
        '6': exit
    }
    while True:
        print_options()
        option = get_user_input()
        try:
            actions[option](path_to_file)
        except KeyError:
            pass


def print_options():
    options = ['Show all tags', 'Show all texts with tags',
               'Remove tag from text', 'Remove tag', 'Add tag to text', 'Exit']
    for pos, option in enumerate(options):
        print(f'{pos + 1}. {option}')


def get_user_input():
    key = getch()
    if key == '\x1b':
        return None
    if key == '\x03':
        exit()
    return key


def remove_tag(path_to_file):
    tag = input("Choose tag: ")
    if tag not in get_all_tags(path_to_file):
        print("Tag doesn't exist")
        return
    texts = get_texts_with_tags(path_to_file)
    if tag in texts:
        del texts[tag]
    save_json(texts, path_to_file)


def remove_tag_from_text(path_to_file):
    tag = input("Choose tag: ")
    if tag not in get_all_tags(path_to_file):
        print("Tag doesn't exist")
        return
    text = input("Choose text: ")
    if text not in get_texts_with_tags(path_to_file).values():
        print("Text doesn't exist")
        return
    texts = get_texts_with_tags(path_to_file)
    try:
        texts[tag].remove(text)
    except Exception:
        pass
    save_json(texts, path_to_file)


def add_tag(path_to_file):
    tag = input("Choose tag: ")
    text = input("Choose text: ")
    if text not in list(get_texts_with_tags(path_to_file).values())[0]:
        print("Text doesn't exist")
        return
    texts = get_texts_with_tags(path_to_file)
    try:
        if tag in texts:
            texts[tag].append(text)
        else:
            texts[tag] = [text]
    except Exception:
        pass
    save_json(texts, path_to_file)


def save_json(texts, path_to_file):
    with open(get_path_to_texts(path_to_file) + "/all_texts.json", 'w') as f:
        json.dump(texts, f)


def get_texts_with_tags(path):
    with open(get_path_to_texts(path) + "/all_texts.json") as f:
        texts = json.load(f)
    return texts


def print_texts(path_to_file):
    for k, v in get_texts_with_tags(path_to_file).items():
        print(f'{k} : {v}')


def get_all_tags(path_to_file):
    with open(get_path_to_texts(path_to_file) + "/all_texts.json") as f:
        tags = list(json.load(f).keys())
    return tags


def print_tags(path_to_file):
    for k in get_all_tags(path_to_file):
        print(k)


def clear():
    os.system('echo -e \\\\033c')


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def get_path_to_texts(dir_name):
    return os.path.dirname(
        os.path.abspath(__file__)) + f'/texts/texts_{dir_name}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default="", help="Directory to texts")
    args = parser.parse_args()
    if not args.d:
        path = os.path.dirname(os.path.abspath(__file__)) + f'/texts'
    path = os.path.basename(args.d)
    main(path)
