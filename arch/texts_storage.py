import json
import os
import random

import arch.settings as sett
import arch.generator as gen


class TextStorage:
    def __init__(self, path=""):
        self.path = os.path.basename(gen.get_path(path))
        self.all_js_path =\
            f'{sett.PATH}/texts/texts_{self.path}/all_texts.json'
        self.base_js_path = f'{sett.PATH}/texts/texts_{self.path}'
        gen.check_texts(path)
        self.labels = self.get_all_labels()

    def add_label(self, text_name, label):
        with open(self.all_js_path) as f:
            labels = json.load(f)
        if label in labels:
            if text_name not in labels[label]:
                labels[label].append(text_name)
        else:
            labels[label] = [text_name]
        with open(self.all_js_path, 'w') as f:
            f.write(json.dumps(labels, ensure_ascii=False))

    def get_all_labels(self):
        with open(self.all_js_path, 'r') as f:
            labels = json.load(f)
        return list(labels.keys())

    def get_text_by_label(self, label):
        with open(self.all_js_path) as f:
            texts = json.load(f)
            if label is None:
                return random.choice(texts['*'])
            twl = texts[label]
            text = random.choice(twl)
            if os.path.exists(
                    f'{self.base_js_path}/json/{text}.json'):
                return text
            return random.choice(texts['*'])

    def get_random_string(self, label):
        text = self.get_text_by_label(label)
        with open(f'{self.base_js_path}/json/{text}.json') \
                as f:
            strings = json.load(f)
            return text, random.choice(strings)

    def get_texts_names(self):
        try:
            with open(self.all_js_path) as f:
                return json.load(f)
        except Exception:
            return []
