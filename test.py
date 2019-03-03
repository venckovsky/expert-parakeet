import unittest
import types
import shelve
import tempfile
import shutil
import indexer as ixr
import tokenizer_1 as atz
import tokenizer_2 as ftz


class IsAlphaTokenizerTest(unittest.TestCase):
    def test_check_input(self):
        with self.assertRaises(TypeError):
            [token.word for token in atz.tokenize(['Человек', 'и', 'кошка'])]

    def test_check_output(self):
        test_case = atz.tokenize('Человек и кошка')
        self.assertIsInstance(test_case, types.GeneratorType)

    def test_basics(self):
        test_string = 'Человек и кошка'
        test_case = [atz.Token(test_string, span) for span in atz.get_span(test_string)]
        self.assertEqual(len(test_case), 3)
        self.assertEqual(test_case[0].word, "Человек")
        self.assertEqual(test_case[0].position, 0)
        self.assertEqual(test_case[1].word, "и")
        self.assertEqual(test_case[1].position, 8)
        self.assertEqual(test_case[2].word, "кошка")
        self.assertEqual(test_case[2].position, 10)


class SymbolTypeTokenizerTest(unittest.TestCase):
    def test_type_list(self):
        with self.assertRaises(TypeError):
            ftz.Tokenizer(['Тетрадь для работ по всему'])

    def test_type_int(self):
        with self.assertRaises(TypeError):
            ftz.Tokenizer(5)

    def test_type_null(self):
        with self.assertRaises(TypeError):
            ftz.Tokenizer()

    def test_basics(self):
        test = ftz.Tokenizer('Wird er auch an seine Grenzen kommen.')
        result = [token for token in test.tokenize()]
        self.assertEqual(len(result), 14)
        self.assertEqual(result[0].substring, "Wird")
        self.assertEqual(result[0].type, "letter")
        self.assertEqual(result[1].substring, " ")
        self.assertEqual(result[1].type, "whitespace")
        self.assertEqual(result[2].substring, "er")
        self.assertEqual(result[2].type, "letter")
        self.assertEqual(result[3].substring, " ")
        self.assertEqual(result[3].type, "whitespace")
        self.assertEqual(result[4].substring, "auch")
        self.assertEqual(result[4].type, "letter")
        self.assertEqual(result[5].substring, " ")
        self.assertEqual(result[5].type, "whitespace")
        self.assertEqual(result[6].substring, "an")
        self.assertEqual(result[6].type, "letter")
        self.assertEqual(result[7].substring, " ")
        self.assertEqual(result[7].type, "whitespace")
        self.assertEqual(result[8].substring, "seine")
        self.assertEqual(result[8].type, "letter")
        self.assertEqual(result[9].substring, " ")
        self.assertEqual(result[9].type, "whitespace")
        self.assertEqual(result[10].substring, "Grenzen")
        self.assertEqual(result[10].type, "letter")
        self.assertEqual(result[11].substring, " ")
        self.assertEqual(result[11].type, "whitespace")
        self.assertEqual(result[12].substring, "kommen")
        self.assertEqual(result[12].type, "letter")
        self.assertEqual(result[13].substring, ".")
        self.assertEqual(result[13].type, "punctuation")

    def test_multichar_punct(self):
        test = ftz.Tokenizer('--seine… Grenzen — kommen...')
        result = [token for token in test.tokenize()]
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].substring, "--")
        self.assertEqual(result[0].type, "punctuation")
        self.assertEqual(result[1].substring, "seine")
        self.assertEqual(result[1].type, "letter")
        self.assertEqual(result[2].substring, "…")
        self.assertEqual(result[2].type, "punctuation")
        self.assertEqual(result[3].substring, " ")
        self.assertEqual(result[3].type, "whitespace")
        self.assertEqual(result[4].substring, "Grenzen")
        self.assertEqual(result[4].type, "letter")
        self.assertEqual(result[5].substring, " ")
        self.assertEqual(result[5].type, "whitespace")
        self.assertEqual(result[6].substring, "—")
        self.assertEqual(result[6].type, "punctuation")
        self.assertEqual(result[7].substring, " ")
        self.assertEqual(result[7].type, "whitespace")
        self.assertEqual(result[8].substring, "kommen")
        self.assertEqual(result[8].type, "letter")
        self.assertEqual(result[9].substring, "...")
        self.assertEqual(result[9].type, "punctuation")

    def test_single_char(self):
        test = ftz.Tokenizer('…')
        result = [token for token in test.tokenize()]
        self.assertEqual(len(result), 1)


class IndexerTest(unittest.TestCase):
    def test_basics(self):
        self.tmp = tempfile.mkdtemp()
        db = ixr.Database(self.tmp + '/test')
        db.add('Wird er auch an seine Grenzen kommen.')
        result = shelve.open(self.tmp + '/test', 'r')
        self.assertEqual(len(result), 7)
        contents = {
            'seine': {'positions': [(16, 21)], 'type': 'letter'},
            'Wird': {'positions': [(0, 4)], 'type': 'letter'},
            'kommen': {'positions': [(30, 36)], 'type': 'letter'},
            'auch': {'positions': [(8, 12)], 'type': 'letter'},
            'Grenzen': {'positions': [(22, 29)], 'type': 'letter'},
            'er': {'positions': [(5, 7)], 'type': 'letter'},
            'an': {'positions': [(13, 15)], 'type': 'letter'}
        }
        self.assertEqual(result, contents)
        result.close()
        shutil.rmtree(self.tmp)

    def test_dict_duplicates(self):
        self.tmp = tempfile.mkdtemp()
        db = ixr.Database(self.tmp + '/test')
        db.add('Nachts da ist der Teufel los! Nachts! 3319 3319 3319')
        result = shelve.open(self.tmp + '/test', 'r')
        self.assertEqual(len(result), 7)
        contents = {
            'los': {'positions': [(25, 28)], 'type': 'letter'},
            'Nachts': {'positions': [(0, 6), (30, 36)], 'type': 'letter'},
            'Teufel': {'positions': [(18, 24)], 'type': 'letter'},
            '3319': {'positions': [(38, 42), (43, 47), (48, 52)], 'type': 'digit'},
            'der': {'positions': [(14, 17)], 'type': 'letter'},
            'ist': {'positions': [(10, 13)], 'type': 'letter'},
            'da': {'positions': [(7, 9)], 'type': 'letter'}}
        self.assertEqual(result, contents)
        result.close()
        shutil.rmtree(self.tmp)


if __name__ == "__main__":
    unittest.main()

