import unittest
import arch.settings as sett


class TestSettings(unittest.TestCase):
    def test_load(self):
        config = sett.load_from_settings()
        self.assertIn('USER', config)
        self.assertIn('STRINGS.RU', config)
        self.assertIn('STRINGS.EN', config)

    def test_change_name(self):
        name = sett.get_name_from_config()
        new_name = 'test'
        sett.change_user(new_name)
        self.assertEqual('test', sett.get_name_from_config())
        sett.change_user(name)
