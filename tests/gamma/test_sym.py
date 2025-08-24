import unittest

import lbd.evaluate as evl
import lbd.gamma as g
import lbd.term as term

N = term.new_name
G = term.new_free_name
F = term.new_abstraction
A = term.new_application


class TestDepth(unittest.TestCase):
    """Test the depth field in name-ASTs.

    Mainly, we want to see if free symbols keep their indices into
    gamma consistent after beta-reduction, as well as to simply check
    if a given lambda term with free symbols parses correctly.

    """

    def test_parse(self):
        decl = "sym x y"
        term = "(\\u.\\v.(u x) y)"

        # Populate gamma.
        evl.eval_raw_term(decl)

        ast = evl.eval_raw_term(term)

        x_index = g.gamma("x")
        y_index = g.gamma("y")

        assert x_index is not None
        assert y_index is not None

        self.assertEqual(ast, F(A(G(y_index, 1),
                                  G(x_index, 1))))
