import re
import unittest

import lbd.evaluate as evl
import lbd.gamma as g
from lbd.prettify import prettify
from tests.gamma.aux import A, F, G, N


class TestPrettifyFree(unittest.TestCase):
    """Test prettification of terms involving free symbols."""

    def tearDown(self):
        g.clear_gamma()

    def test_free_symbols(self):
        """Test prettification of free symbols."""

        evl.eval_raw_term("def x := \\x.x")
        evl.eval_raw_term("def y := \\x.x")

        x_index = g.gamma("x")
        y_index = g.gamma("y")

        assert x_index is not None
        assert y_index is not None

        # (\u.\v.(u x) y)
        term = A(F(F(A(N(1, 2),
                       G(x_index, 2)))),
                 G(y_index, 0))

        pretty = prettify(term)
        pattern = r"""\(\\(\w+)\.\\(\w+)\.\(\1\n\s+X\)\n\s+Y\)"""

        mobj = re.fullmatch(pattern, pretty)

        self.assertIsNotNone(mobj)
