import unittest

import lbd.error as err
import lbd.evaluate as evl
import lbd.tokenize as tkz
from lbd.term import IDENTITY


class TestDefaultValue(unittest.TestCase):
    def test_default_value(self):
        term = "sym a; a"

        tokens = tkz.tokenize(term)

        assert not isinstance(tokens, err.LambdaError)

        ast = evl.eval_line(tokens)

        self.assertEqual(ast, IDENTITY)
