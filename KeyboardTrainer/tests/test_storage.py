import unittest
import os
import json
from arch.texts_storage import TextStorage

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestStorage(unittest.TestCase):
    def test_create(self):
        storage = TextStorage()
        self.assertEqual(storage.path, "")
        self.assertEqual(storage.all_js_path,
                         f'{PATH}/texts/texts_/all_texts.json')

    def test_labels(self):
        storage = TextStorage(f'{PATH}/tests/test/')
        self.assertEqual(storage.path, 'test')
        self.assertEqual(storage.all_js_path,
                         f'{PATH}/texts/texts_test/all_texts.json')
        self.assertIn('*', storage.get_all_labels())

    def test_add(self):
        storage = TextStorage(f'{PATH}/tests/test/')
        storage.add_label('test1', 'test')
        self.assertIn('*', storage.get_all_labels())
        self.assertIn('test', storage.get_all_labels())

    def test_get(self):
        storage = TextStorage(f'{PATH}/tests/test/')
        storage.add_label('test1', 'test')
        self.assertIn('test1', storage.get_text_by_label('test'))

    def test_get_names(self):
        storage = TextStorage(f'{PATH}/tests/test/')
        storage.add_label('test1', 'test')
        d = {'*': ['test1', 'test2'], "test": ['test1']}
        self.assertDictEqual(d, storage.get_texts_names())

    def test_get_random_string(self):
        storage = TextStorage(f'{PATH}/tests/test/')
        storage.add_label('test1', 'test')
        text, string = storage.get_random_string('test')
        with open(f'{PATH}/texts/texts_test/json/test1.json') as f:
            alls = json.load(f)
        self.assertIn(string, alls)
        self.assertIn(text, storage.get_texts_names()['*'])
