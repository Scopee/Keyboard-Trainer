import json
import random
import os


class Generator:
    @staticmethod
    def generate_text(file):
        with open(file) as f:
            text = f.read().split('\n')
            result = []
            for line in text:
                length = len(
                    line.replace('!', '.').replace('?', '.').split('.'))
                if length > 4 and len(line) > 70 and not line.startswith('– '):
                    line = line[:250]
                    index = line.rfind('.')
                    line_to_append = line[:index]
                    result.append(
                        line_to_append.replace('«', "\"")
                        .replace('–', '-')
                        .replace('»', '\"') + '.')
                    continue
                if len(line) < 70 or line.startswith('– ') or length < 2:
                    continue
                result.append(line.replace('«', "\"")
                              .replace('–', '-')
                              .replace('»', '\"'))
        return result

    @staticmethod
    def generate_json(text):
        return json.dumps(text, ensure_ascii=False)

    @staticmethod
    def write_json(file, filename):
        with open('./texts/json/{}.json'.format(filename), 'w') as f:
            f.write(Generator.generate_json(Generator.generate_text(file)))
        with open('./texts/all_texts.json') as f:
            js = f.read()
            if js:
                jsons = json.loads(js)
                if filename not in jsons:
                    jsons.append(filename)
            else:
                jsons = [filename]
        with open('./texts/all_texts.json', 'w') as f:
            f.write(json.dumps(jsons))

    @staticmethod
    def get_texts_names():
        with open('./texts/all_texts.json') as f:
            js = f.read()
            if js:
                return json.loads(js)
            return []

    @staticmethod
    def get_random_text():
        with open('./texts/all_texts.json') as f:
            texts = json.loads(f.read())
            return random.choice(texts)

    @staticmethod
    def get_random_string():
        text = Generator.get_random_text()
        with open('./texts/json/{}.json'.format(text)) as f:
            strings = json.loads(f.read())
            return random.choice(strings)

    @staticmethod
    def check_texts():
        files = os.listdir('./texts')
        texts = filter(lambda x: os.path.splitext(x)[1] == '.txt', files)
        names = list(map(lambda x: os.path.splitext(x)[0], texts))
        all_text_names = Generator.get_texts_names()
        for i in names:
            if i not in all_text_names:
                Generator.write_json('./texts/{}.txt'.format(i), i)
