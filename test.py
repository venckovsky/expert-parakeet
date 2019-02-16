import unittest, types
import tokenizer_1 as tz


class Test(unittest.TestCase):
    def test_check_input(self):
        with self.assertRaises(TypeError):
            [token.word for token in tz.tokenize(['Человек', 'и', 'кошка'])]

    def check_output(self):
        test_case = tz.tokenize('Человек и кошка')
        self.assertIsInstance(test_case, types.GeneratorType)

    def test_basics(self):
        test_string = 'Человек и кошка'
        test_case = [tz.Token(test_string, span) for span in tz.get_span(test_string)]
        self.assertEqual(len(test_case), 3)
        self.assertEqual(test_case[0].word, "Человек")
        self.assertEqual(test_case[0].position, 0)
        self.assertEqual(test_case[1].word, "и")
        self.assertEqual(test_case[1].position, 8)
        self.assertEqual(test_case[2].word, "кошка")
        self.assertEqual(test_case[2].position, 10)


if __name__ == "__main__":
    unittest.main()
