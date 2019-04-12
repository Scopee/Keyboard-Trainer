import unittest
from arch.userinput import UserInput


class InputTest(unittest.TestCase):

    def test_create(self):
        inp = UserInput('test')
        self.assertEqual('test', inp.text)

    def test_update_one_correct_symbol(self):
        inp = UserInput('test')
        inp.update('t')
        self.assertEqual('t', inp.correct_text())
        self.assertEqual('', inp.incorrect_text)

    def test_update_one_incorrect_symbol(self):
        inp = UserInput('test')
        inp.update('a')
        self.assertEqual('', inp.correct_text())
        self.assertEqual('a', inp.incorrect_text)

    def test_update_all_correct_symbols(self):
        string = 'test'
        inp = UserInput(string)
        for s in string:
            inp.update(s)
        self.assertEqual(string, inp.correct_text())

    def test_many_incorrect_symbols(self):
        string = 'test'
        wrong_string = 'qwry '
        inp = UserInput(string)
        for s in wrong_string:
            inp.update(s)
        self.assertEqual(wrong_string, inp.incorrect_text)
        self.assertEqual('', inp.correct_text())

    def test_two_words(self):
        string = 'abc cde'
        inp = UserInput(string)
        for s in string[:4]:
            inp.update(s)
        self.assertEqual('abc ', inp.correct_text())
        self.assertEqual('', inp.correct_input)

    def test_backspace(self):
        string = 'test'
        inp = UserInput(string)
        inp.update('\x1b')
        self.assertEqual('', inp.correct_input)
        self.assertEqual('', inp.incorrect_text)

    def test_backspace_after_word(self):
        string = 'test test'
        inp = UserInput(string)
        for s in string[:5]:
            inp.update(s)
        inp.update('\x1b')
        self.assertEqual('', inp.correct_input)
        self.assertEqual('', inp.incorrect_text)