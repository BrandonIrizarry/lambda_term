import unittest

import lbd.tokenize as tkz


class TestTokenizer(unittest.TestCase):
    def test_identity(self):
        raw_term = "\\x.x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.spec["lambda"],
            tkz.name_t("x"),
            tkz.spec["dot"],
            tkz.name_t("x"),
        ]

        self.assertEqual(tokens,  expected)

    def test_def(self):
        raw_term = "def id x := x"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.spec["def"],
            tkz.name_t("id"),
            tkz.name_t("x"),
            tkz.spec["assign"],
            tkz.name_t("x"),
        ]

        self.assertEqual(tokens, expected)

    def test_application(self):
        raw_term = "(select_first x y)"

        tokens = tkz.tokenize(raw_term)
        expected = [
            tkz.spec["left_paren"],
            tkz.name_t("select_first"),
            tkz.name_t("x"),
            tkz.name_t("y"),
            tkz.spec["right_paren"],
        ]

        self.assertEqual(tokens, expected)
