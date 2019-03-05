import shelve
from tokenizer_2 import Tokenizer


class Database:
    def __init__(self, db):
        self.db = shelve.open(db, writeback=True)

    def add(self, text):
        for token in Tokenizer(text).tokenize():
            if token.type == 'digit' or token.type == 'letter':
                self.db.setdefault(token.substring, {}).setdefault('positions', [])
                self.db[token.substring]['positions'].append(token.span)
                self.db[token.substring]['type'] = token.type
        self.db.sync()
