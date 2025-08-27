import re
import unittest

import lbd.evaluate as evl
import lbd.gamma as g
import lbd.prettify as prettify
from tests.aux import A, F, G, N

identity = F(N(0, 1))

selectors = {
    "first": F(F(F(N(2, 3)))),
    "second": F(F(F(N(1, 3)))),
    "third": F(F(F(N(0, 3)))),
}


class TestPrettify(unittest.TestCase):
    def test_identity(self):
        """Test prettified identity function."""

        pretty_id = prettify.prettify(identity)

        mobj = re.fullmatch(r"\\(\w+)\.\1", pretty_id)

        self.assertIsNotNone(mobj)

    def test_selectors(self):
        """Test 'select_first', 'select_second', and 'select_third'."""

        for i, (ordinal, _) in enumerate(selectors.items()):
            pretty = prettify.prettify(selectors[ordinal])
            mobj = re.fullmatch(
                rf"\\(\w+)\.\\(\w+)\.\\(\w+)\.\{i + 1}", pretty)

            self.assertIsNotNone(mobj)

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

        g.clear_gamma()
