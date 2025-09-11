import unittest

from lbd.token_defs import Tk
from lbd.tokenize import Token, tokenize


class TestTokenizer(unittest.TestCase):
    """Lambda Term tokenizer module."""

    def test_identity(self):
        raw_term = "\\x.x"

        tokens = tokenize(raw_term)
        expected = [
            Token(Tk.LAMBDA),
            Token(Tk.NAME, "x"),
            Token(Tk.DOT),
            Token(Tk.NAME, "x"),
        ]

        self.assertEqual(tokens,  expected)

    def test_application(self):
        raw_term = "(select_first x y)"

        tokens = tokenize(raw_term)
        expected = [
            Token(Tk.LEFT_PAREN),
            Token(Tk.NAME, "select_first"),
            Token(Tk.NAME, "x"),
            Token(Tk.NAME, "y"),
            Token(Tk.RIGHT_PAREN),
        ]

        self.assertEqual(tokens, expected)

    def test_line_breaks(self):
        """Tokenizer accepts expressions with line breaks."""

        term = """
\\u.\\x.(u
         x)
"""

        tokens = tokenize(term)
        expected = [
            Token(Tk.LAMBDA),
            Token(Tk.NAME, "u"),
            Token(Tk.DOT),
            Token(Tk.LAMBDA),
            Token(Tk.NAME, "x"),
            Token(Tk.DOT),
            Token(Tk.LEFT_PAREN),
            Token(Tk.NAME, "u"),
            Token(Tk.NAME, "x"),
            Token(Tk.RIGHT_PAREN),
        ]

        self.assertEqual(expected, tokens)
