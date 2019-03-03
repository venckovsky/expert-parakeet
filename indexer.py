import shelve
from tokenizer_2 import Tokenizer


class Database:
    def __init__(self, db):
        self.db = db

    def add(self, text):
        with shelve.open(self.db, writeback=True) as database:
            for token in Tokenizer(text).tokenize():
                if token.type == 'digit' or token.type == 'letter':
                    database.setdefault(token.substring, {})
                    database[token.substring].setdefault('positions', [])
                    database[token.substring]['positions'].append(token.span)
                    database[token.substring]['type'] = token.type
            print(dict(database))
            database.close()
