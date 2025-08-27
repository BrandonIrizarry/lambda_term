import unittest

import lbd.error as err
import lbd.evaluate as evl
import lbd.gamma as g
import lbd.tokenize as tkz
from tests.aux import F, G, N, S


class TestSemicolon(unittest.TestCase):
    """Test using a semicolon to delimit terms occurring on the same
    line in the REPL.

    """

    def test_simple_sym(self):
        term = "sym u; \\x.u"
        tokens = tkz.tokenize(term)

        assert not isinstance(tokens, err.LambdaError)

        ast = evl.eval_line(tokens)

        assert not isinstance(ast, err.LambdaError)

        expected = F(G(0, 1))

        self.assertEqual(ast, expected)

        g.clear_gamma()
