import re
import unittest

import lbd.evaluate as evl
import lbd.gamma as g
import lbd.prettify as prettify
from tests.aux import A, F, G, N


class TestPrettifyFree(unittest.TestCase):
    """Test prettification of terms involving free symbols."""

    def tearDown(self):
        g.clear_gamma()

    def test_free_symbols(self):
        """Test prettification of free symbols."""

        evl.eval_raw_term("sym x y")

        x_index = g.gamma("x")
        y_index = g.gamma("y")

        assert x_index is not None
        assert y_index is not None

        term = A(F(F(A(N(1, 2),
                       G(x_index, 2)))),
                 G(y_index, 0))

        pretty = prettify.prettify(term)
        pattern = r"\(\\(\w+)\.\\(\w+)\.\(\1 X\) Y\)"

        mobj = re.fullmatch(pattern, pretty)

        self.assertIsNotNone(mobj)
