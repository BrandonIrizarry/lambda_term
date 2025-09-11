import unittest

import lbd.tokenize as tkz
from lbd.token_defs import Tk


class TestTokenizer(unittest.TestCase):
    """Lambda Term tokenizer module."""

    def test_identity(self):
        raw_term = "\\x.x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.spec["lambda"],
            tkz.Token(Tk.NAME, "x"),
            tkz.spec["dot"],
            tkz.Token(Tk.NAME, "x"),
        ]

        self.assertEqual(tokens,  expected)

    def test_application(self):
        raw_term = "(select_first x y)"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.spec["left_paren"],
            tkz.Token(Tk.NAME, "select_first"),
            tkz.Token(Tk.NAME, "x"),
            tkz.Token(Tk.NAME, "y"),
            tkz.spec["right_paren"],
        ]

        self.assertEqual(tokens, expected)

    def test_line_breaks(self):
        """Tokenizer accepts expressions with line breaks."""

        term = """
\\u.\\x.(u
         x)
"""

        tokens = tkz.tokenize(term)
        expected = [
            tkz.spec["lambda"],
            tkz.Token(Tk.NAME, "u"),
            tkz.spec["dot"],
            tkz.spec["lambda"],
            tkz.Token(Tk.NAME, "x"),
            tkz.spec["dot"],
            tkz.spec["left_paren"],
            tkz.Token(Tk.NAME, "u"),
            tkz.Token(Tk.NAME, "x"),
            tkz.spec["right_paren"],
        ]

        self.assertEqual(expected, tokens)
