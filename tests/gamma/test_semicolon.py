import unittest

import lbd.error as err
import lbd.evaluate as evl
import lbd.gamma as g
import lbd.tokenize as tkz
from tests.gamma.aux import F, G


class TestSemicolon(unittest.TestCase):
    """Test using a semicolon to delimit terms occurring on the same
    line in the REPL.

    """

    def tearDown(self):
        g.clear_gamma()

    def test_simple_sym(self):
        term = "<u \\x.x>; \\x.u"
        tokens = tkz.tokenize(term)

        assert not isinstance(tokens, err.LambdaError)

        ast = evl.eval_line(tokens)

        assert not isinstance(ast, err.LambdaError)

        expected = F(G(0, 1))

        self.assertEqual(ast, expected)
