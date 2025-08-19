import unittest

import lbd.tokenize_lambda as tkz

LAMBDA = tkz.Token(tkz.Tk.LAMBDA)
DOT = tkz.Token(tkz.Tk.DOT)
DEF = tkz.Token(tkz.Tk.DEF)
ASSIGN = tkz.Token(tkz.Tk.ASSIGN)
LEFT_PAREN = tkz.Token(tkz.Tk.LEFT_PAREN)
RIGHT_PAREN = tkz.Token(tkz.Tk.RIGHT_PAREN)


def name_t(value: str):
    return tkz.Token(tkz.Tk.NAME, value)


class TestTokenizer(unittest.TestCase):
    def test_identity(self):
        raw_term = "\\x.x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            LAMBDA,
            name_t("x"),
            DOT,
            name_t("x"),
        ]

        self.assertEqual(tokens,  expected)

    def test_def(self):
        raw_term = "def id x := x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            DEF,
            name_t("id"),
            name_t("x"),
            ASSIGN,
            name_t("x")
        ]

        self.assertEqual(tokens, expected)

    def test_application(self):
        raw_term = "(select_first x y)"

        tokens = tkz.tokenize(raw_term)
        expected = [
            LEFT_PAREN,
            name_t("select_first"),
            name_t("x"),
            name_t("y"),
            RIGHT_PAREN

        ]

        self.assertEqual(tokens, expected)
