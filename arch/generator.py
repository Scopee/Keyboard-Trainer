import json
import random
import os


# TODO '''
# Просится такая декомпозиция:
#
# Нечто, чистящее текст и разбивающее его по предложениям
# Нечто, принимающее на вход список предложений и выдаёт
# некоторый набор предложений для набора
#
# '''
class Generator:
    @staticmethod
    def generate_text(file):
        sentences = Generator \
            .clear_sentences(Generator.get_sentences(file))
        res = []
        for i in range(len(sentences)):
            st = ''
            rd = random.randint(2, 3)
            for j in range(rd):
                if i + j < len(sentences):
                    st += sentences[i + j] + ' '
            st = st[:-1]
            res.append(st)
            i += rd + 1
        return res

    @staticmethod
    def clear_sentences(sentences):
        sentences = map(lambda x: x + '.', sentences)
        return list(map(lambda x: x.replace('«', "\"")
                        .replace('–', '-')
                        .replace('»', '\"'), sentences))

    @staticmethod
    def get_sentences(file):
        with open(file) as f:
            text = f.read()
            text = text.replace('!', '.').replace('?', '.').replace('\n', '')
            text = text.split('.')
            text = filter(lambda x: x, text)
            text = filter(lambda x: x[0].isupper(), text)
        return list(text)

    @staticmethod
    def clear_text(text):
        text.replace('«', "\"") \
            .replace('–', '-') \
            .replace('»', '\"')

    @staticmethod
    def generate_json(text):
        return json.dumps(text, ensure_ascii=False)

    @staticmethod
    def write_json(file, filename):
        with open('./texts/json/{}.json'.format(filename), 'w') as f:
            f.write(Generator.generate_json(Generator.generate_text(file)))
        try:
            with open('./texts/all_texts.json') as f:
                jsons = json.load(f)
                if filename not in jsons:
                    jsons.append(filename)
        except FileNotFoundError:
            jsons = [filename]
        with open('./texts/all_texts.json', 'w') as f:
            f.write(json.dumps(jsons))

    @staticmethod
    def get_texts_names():
        try:
            with open('./texts/all_texts.json') as f:
                return json.load(f)
        except FileNotFoundError:
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
            strings = json.load(f)
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
