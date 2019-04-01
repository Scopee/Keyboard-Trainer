class UserInput:
    def __init__(self, text):
        self._text = text.split(' ')
        for i in range(0, len(self._text) - 1):
            self._text[i] = self._text[i] + ' '
        self._input = ''
        self._word = ''
        self._error_idx = 0
        self._word_idx = 0
        self._correct_text = ''
        self._incorrect_text = ''
        self._is_error = False

    @property
    def text(self):
        return ''.join(self._text)

    @property
    def input(self):
        return self._input

    @property
    def correct_input(self):
        return self._correct_text

    @property
    def correct_text(self):
        res = ''
        for i in range(0, self._word_idx):
            res += self._text[i]
        res += self._correct_text
        return res

    @property
    def get_black_text(self):
        if self._word_idx < len(self._text):
            if self._incorrect_text:
                res = self._text[self._word_idx][len(self._correct_text) + 1:]
            else:
                res = self._text[self._word_idx][len(self._correct_text):]
            for i in range(self._word_idx + 1, len(self._text)):
                res += self._text[i]
            return res
        return ''

    @property
    def incorrect_text(self):
        return self._incorrect_text

    @property
    def get_incorrect_symbol(self):
        if len(self._incorrect_text) > 0:
            return self._text[self._word_idx][self._error_idx]
        return ''

    @property
    def is_error(self):
        return self._is_error

    def update_word(self, symbol):
        if bytes(symbol, encoding='utf8') == b'\x7f':
            if self._error_idx > 0 or self._word:
                self._word = self._word[0: len(self._word) - 1]
                if len(self._incorrect_text) == 0:
                    self._error_idx -= 1
                    self._correct_text = self._correct_text[0: len(self._correct_text) - 1]
                elif self._incorrect_text:
                    self._incorrect_text = self._incorrect_text[0: len(self._incorrect_text) - 1]
        elif symbol == self._text[self._word_idx][self._error_idx] and not self._incorrect_text:
            self._word += symbol
            self._correct_text += symbol
            self._input += symbol
            self._error_idx += 1
        elif symbol != self._text[self._word_idx][self._error_idx]:
            self._incorrect_text += symbol
            self._word += symbol

    def update(self, symbol):
        self.update_word(symbol)
        if self.word_done():
            self._word_idx += 1
            self._error_idx = 0
            self._word = ''
            self._correct_text = ''

    def word_done(self):
        return self._text[self._word_idx] == self._word

    def is_done(self):
        return self._word_idx == len(self._text)


'''
        if bytes(symbol, encoding='utf8') == b'\x7f':
            if self.text[self._error_idx] != ' ':
                self._input = self._input[0: len(self._input) - 1]
            if len(self._incorrect_text) == 0:
                self._error_idx -= 1
                self._correct_text = self._correct_text[0: len(self._correct_text) - 1]
            else:
                self._incorrect_text = self._incorrect_text[0: len(self._incorrect_text) - 1]
        elif bytes(symbol, encoding='utf8') == b' ' and len(self._incorrect_text) == 0:
            self._correct_text = ''
            self._input += symbol
        elif symbol == self.text[self._error_idx] and len(self._incorrect_text) == 0:
            self._error_idx += 1
            self._correct_text += symbol
            self._input += symbol
        elif symbol != self.text[self._error_idx]:
            self._incorrect_text += symbol
            self._input += symbol'''
