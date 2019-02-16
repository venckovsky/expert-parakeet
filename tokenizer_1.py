
"""
This tokenizer divides a text into words by using String isalpha() method.
It iterates through the text and checks whether each symbol is an alphabetic character.
"""


class Token:
    """
    Defines two main properties of a token.
    Given a span of a token and the text, returns a word token and its position.
    """
    def __init__(self, text, span):
        self.__text = text
        self.__span = span

    @property
    def word(self):
        return self.__text[self.__span[0]:self.__span[1]]

    @property
    def position(self):
        return self.__span[0]


def get_span(input_string):
    """
    Iterates through pairs of symbols.
    For each of them checks, whether they are alphabetic.
    A combination of a non-alphabetic and an alphabetic character is considered to be a beginning of a token.
    An alphabetical and a non-alphabetical characters together mark the end of a token.
    :param input_string:
    :return: yields a tuple with a span
    """
    if not isinstance(input_string, str):
        raise TypeError('Invalid type of input')

    span_beginning = 0
    span_ending = 0
    for el in range(len(input_string) - 1):
        # if two symbols are a combination of a non-alphabetic and an alphabetic character,
        # get_span() records the index of a non-alphabetic character as a span_ending
        if input_string[el].isalpha() and not input_string[el + 1].isalpha():
            span_ending = el + 1
            # filter out the wrong spans
            if span_beginning < span_ending:
                yield(span_beginning, span_ending)
        # if two symbols are a combination of an alphabetic and a non-alphabetic character,
        # get_span() records the index of an alphabetic character as a span_beginning
        if not input_string[el].isalpha() and input_string[el + 1].isalpha():
            span_beginning = el + 1
            # filter out the wrong spans
            if span_beginning < span_ending:
                yield(span_beginning, span_ending)
    yield (span_beginning, len(input_string))


def tokenize(input_string):
    for span in get_span(input_string):
        yield Token(input_string, span)

