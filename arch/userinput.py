class UserInput:
    def __init__(self, text):
        self._words = UserInput.get_words(text)
        self._input = ''
        self._word = ''
        self._error_idx = 0
        self._word_idx = 0
        self._correct_text = ''
        self._incorrect_text = ''
        self._error_count = 0
        self._count = 0

    @property
    def text(self):
        return ''.join(self._words)

    @property
    def correct_input(self):
        return self._correct_text

    @property
    def incorrect_text(self):
        return self._incorrect_text

    @property
    def error_count(self):
        return self._error_count

    @property
    def count(self):
        return self._count

    @property
    def accurate(self):
        return (len(self.text) - self._error_count) / len(self.text)

    @staticmethod
    def get_words(text):
        raw_words = text.split(' ')
        words = list(map(lambda x: x + ' ', raw_words))
        words[-1] = words[-1][:-1]
        return words

    def correct_text(self):
        return ''.join(self._words[:self._word_idx]) + self._correct_text

    def get_blank_text(self):
        if self._word_idx < len(self._words):
            word = self._words[self._word_idx]
        else:
            return ''
        if self._incorrect_text:
            res = word[len(self._correct_text) + 1:]
        else:
            res = word[len(self._correct_text):]
        for i in range(self._word_idx + 1, len(self._words)):
            res += self._words[i]
        return res

    def get_incorrect_symbol(self):
        if len(self._incorrect_text) > 0:
            return self._words[self._word_idx][self._error_idx]
        return ''

    def update_word(self, symbol):
        if symbol == '\x1b':
            return
        if symbol == '\x7f':
            if self._error_idx > 0 or self._word:
                self._word = self._word[0: len(self._word) - 1]
                if len(self._incorrect_text) == 0:
                    self._error_idx -= 1
                    self._correct_text = self._correct_text[:-1]
                elif self._incorrect_text:
                    self._incorrect_text = self._incorrect_text[:-1]
        elif symbol == self._words[self._word_idx][self._error_idx] \
                and not self._incorrect_text:
            self._word += symbol
            self._correct_text += symbol
            self._input += symbol
            self._error_idx += 1
            self._count += 1
        elif symbol != self._words[self._word_idx][self._error_idx]:
            self._error_count += 1
            self._incorrect_text += symbol
            self._word += symbol

    def update(self, symbol):
        self.update_word(symbol)
        if self.is_word_done():
            self._word_idx += 1
            self._error_idx = 0
            self._word = ''
            self._correct_text = ''

    def is_word_done(self):
        return self._words[self._word_idx] == self._word

    def is_done(self):
        return self._word_idx == len(self._words)
