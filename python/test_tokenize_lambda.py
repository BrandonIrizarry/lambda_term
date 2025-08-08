import unittest

import tokenize_lambda as tkz


class TestTokenizer(unittest.TestCase):
    def test_identity(self):
        raw_term = "\\x.x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            {"kind": tkz.Token.LAMBDA},
            {"kind": tkz.Token.NAME, "value": "x"},
            {"kind": tkz.Token.DOT},
            {"kind": tkz.Token.NAME, "value": "x"}
        ]

        self.assertEqual(tokens,  expected)
