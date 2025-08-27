import unittest

import lbd.evaluate as evl
import lbd.gamma as g
from tests.aux import A, F, G


class TestDepth(unittest.TestCase):
    """Test the depth field in name-ASTs.

    Mainly, we want to see if free symbols keep their indices into
    gamma consistent after beta-reduction, as well as to simply check
    if a given lambda term with free symbols parses correctly.

    """

    def tearDown(self):
        # We must clear gamma - otherwise, the other tests will take
        # these free symbols as having been declared!
        g.clear_gamma()

    def test_parse(self):
        decl = "sym x y"
        term = "(\\u.\\v.(u x) y)"

        # Populate gamma.
        evl.eval_raw_term(decl)

        ast = evl.eval_raw_term(term)

        x_index = g.gamma("x")
        y_index = g.gamma("y")

        self.assertEqual(x_index, 0)
        self.assertEqual(y_index, 1)

        assert x_index is not None
        assert y_index is not None

        self.assertEqual(ast, F(A(G(y_index, 1),
                                  G(x_index, 1))))
