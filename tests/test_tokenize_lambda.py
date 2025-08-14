import unittest

import lbd.tokenize_lambda as tkz


class TestTokenizer(unittest.TestCase):
    def test_identity(self):
        raw_term = "\\x.x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.lambda_t(),
            tkz.name_t("x"),
            tkz.dot_t(),
            tkz.name_t("x")
        ]

        self.assertEqual(tokens,  expected)

    def test_def(self):
        raw_term = "def id x := x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.def_t(),
            tkz.name_t("id"),
            tkz.name_t("x"),
            tkz.assign_t(),
            tkz.name_t("x")
        ]

        self.assertEqual(tokens, expected)

    def test_application(self):
        raw_term = "(select_first x y)"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.left_paren_t(),
            tkz.name_t("select_first"),
            tkz.name_t("x"),
            tkz.name_t("y"),
            tkz.right_paren_t()
        ]

        self.assertEqual(tokens, expected)
