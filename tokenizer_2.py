import unicodedata


class Symbol:
    def __init__(self, symbol):
        """
        Defining the Token class: it stores the information about the type of
        the substring, its content, and the position of its first symbol
        """
        # records the type of the symbols
        self.symbol = symbol

    @property
    def type(self):
        if self.symbol.isalpha():
            return 'letter'
        # type is 'digit' if the symbol is a digit
        elif self.symbol.isdigit():
            return 'digit'
        # type is 'whitespace' if the symbol is a whitespace
        elif self.symbol.isspace():
            return 'whitespace'
            # type is 'punctuation' if the symbol is a punctuation mark
        elif unicodedata.category(self.symbol)[0] == 'P':
            return 'punctuation'
        else:
            # type is 'other' by default
            return 'other'


class Token:
    def __init__(self, substring, span, symboltype):
        """
        Defining the Token class: it stores the information about the type of
        the substring, its content, and the position of its first symbol
        """
        # a substring where all symbols belong to the same type
        self.substring = substring
        # records the position of the substring's first symbol
        self.span = span
        # records the type of the symbols
        self.type = symboltype


class Tokenizer:
    def __init__(self, text):
        self.text = text
        if not isinstance(self.text, str) or len(self.text) < 1:
            raise TypeError('Wrong input')

    def tokenize(self):
        first_symbol, first_symbol_position = self.text[0], 0
        for num, sym in enumerate(self.text):
            first_sym_aug, current_sym = Symbol(first_symbol), Symbol(sym)
            # if the type of the current symbol is different from the type of
            # the first symbol of the current token, then the current token has
            # ended and the current symbol is the first symbol of the next token
            if num != first_symbol_position and current_sym.type != first_sym_aug.type:
                yield Token(self.text[first_symbol_position:num],
                            (first_symbol_position, num),
                            first_sym_aug.type)
                first_symbol = sym
                first_symbol_position = num
            # this catches the last token
            if num + 1 == len(self.text):
                yield Token(self.text[first_symbol_position:num + 1],
                            (first_symbol_position, num + 1),
                            current_sym.type)
