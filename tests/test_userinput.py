from arch.userinput import UserInput


def test_create():
    inp = UserInput('test')
    assert 'test' == inp.text


def test_update_one_correct_symbol():
    inp = UserInput('test')
    inp.update('t')
    assert 't' == inp.correct_text()
    assert '' == inp.incorrect_text


def test_update_one_incorrect_symbol():
    inp = UserInput('test')
    inp.update('a')
    assert '' == inp.correct_text()
    assert 'a' == inp.incorrect_text


def test_update_all_correct_symbols():
    string = 'test'
    inp = UserInput(string)
    for s in string:
        inp.update(s)
    assert string == inp.correct_text()


def test_many_incorrect_symbols():
    string = 'test'
    wrong_string = 'qwry '
    inp = UserInput(string)
    for s in wrong_string:
        inp.update(s)
    assert wrong_string == inp.incorrect_text
    assert '' == inp.correct_text()


def test_two_words():
    string = 'abc cde'
    inp = UserInput(string)
    for s in string[:4]:
        inp.update(s)
    assert 'abc ' == inp.correct_text()
    assert '' == inp.correct_input


def test_backspace():
    string = 'test'
    inp = UserInput(string)
    inp.update('\x7f')
    assert '' == inp.correct_input
    assert '' == inp.incorrect_text


def test_del_backspace():
    string = 'test'
    inp = UserInput(string)
    inp.update('t')
    inp.update('\x7f')
    assert '' == inp.correct_input
    assert '' == inp.incorrect_text


def test_backspace_after_word():
    string = 'test test'
    inp = UserInput(string)
    for s in string[:5]:
        inp.update(s)
    inp.update('\x7f')
    assert '' == inp.correct_input
    assert '' == inp.incorrect_text
