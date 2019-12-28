import unittest
from arch.user import User
from arch.userinput import UserInput
import arch.settings as sett


class TestUser(unittest.TestCase):
    def test_create(self):
        old_nick = sett.get_name_from_config()
        sett.change_user('test')
        user = User('test')
        self.assertEqual('test', user.name)
        stat_names = ['text_count', 'symbol_count', 'errors', 'average_speed',
                      'average_errors', 'max_speed', 'dynamic']
        for name in stat_names:
            self.assertIn(name, user.stat)
        sett.change_user(old_nick)

    def test_update(self):
        old_nick = sett.get_name_from_config()
        sett.change_user('test')
        user = User('test')
        old_tcount = user.stat['text_count']
        old_count = user.stat['symbol_count']
        old_errors = user.stat['errors']
        string = 'test'
        inp = UserInput(string)
        for s in string:
            inp.update(s)
        user.update_stat(inp, 1, 100)
        stat = user.load_statistics()
        self.assertEqual(old_tcount + 1, stat['text_count'])
        self.assertEqual(old_count + len(string),
                         stat['symbol_count'])
        self.assertEqual(old_errors, stat['errors'])
        sett.change_user(old_nick)
