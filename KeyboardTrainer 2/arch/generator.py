import json
import random
import os
import arch.settings as s

DEFAULT_DIR = f'{s.PATH}/texts'


def create_texts(file):
    sentences = clear_sentences(get_sentences(file))
    res = []
    for i in range(len(sentences)):
        rd = random.randint(2, 3)
        res.append(' '.join(sentences[i:i + rd]))
    return res


def clear_sentences(sentences):
    sentences = map(lambda x: x + '.', sentences)
    return list(map(lambda x: x.replace('«', "\"")
                    .replace('–', '-')
                    .replace('»', '\"'), sentences))


def get_sentences(file):
    with open(file) as f:
        text = f.read()
        text = text.replace('!', '.').replace('?', '.').replace('\n', '')
        text = text.split('.')
        text = filter(None, text)
        text = map(lambda x: x.lstrip(), text)
    return list(text)


def generate_json(text):
    return json.dumps(text, ensure_ascii=False)


def write_json(fr, text_name, dir_name):
    os.makedirs(f'{path_to_texts(dir_name)}/json', exist_ok=True)
    with open(f'{path_to_texts(dir_name)}/json/{text_name}.json', 'w') \
            as f:
        f.write(generate_json(create_texts(fr)))
    try:
        with open(f'{path_to_texts(dir_name)}/all_texts.json') as f:
            jsons = json.load(f)
            if text_name not in jsons['*']:
                jsons['*'].append(text_name)
    except (json.decoder.JSONDecodeError, IOError):
        jsons = {'*': [text_name]}

    with open(f'{path_to_texts(dir_name)}/all_texts.json', 'w') as f:
        f.write(json.dumps(jsons))


def write_labels(labels, dir_name):
    del labels['*']
    with open(f'{path_to_texts(dir_name)}/all_texts.json', 'r') as f:
        js = json.load(f)
    js.update(labels)
    with open(f'{path_to_texts(dir_name)}/all_texts.json', 'w') as f:
        f.write(json.dumps(js))


def check_texts(dir_name):
    if os.path.exists(get_path(dir_name)):
        files = os.listdir(get_path(dir_name))
    else:
        files = os.listdir(get_path(DEFAULT_DIR))
        files = map(lambda x: f'{s.PATH}/texts/{x}', files)
    fi = []
    files = filter(lambda x: os.path.splitext(x)[1] == ".txt", files)
    for n in files:
        fi.append((os.path.splitext(os.path.basename(n))[0],
                   f'{get_path(dir_name)}/{n}'))
    d = os.path.basename(get_path(dir_name))
    for n, p in fi:
        write_json(p, n, d)


def get_path(path):
    path = f'{os.path.dirname(path)}/{os.path.basename(path)}'
    return path[:-1] if path[-1] == "/" else path


def path_to_texts(dir_name):
    return f'{s.PATH}/texts/texts_{dir_name}'
