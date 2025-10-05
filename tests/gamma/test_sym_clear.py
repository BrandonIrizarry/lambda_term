import unittest

import lbd.gamma as gamma
from lbd.term import Empty
from tests.gamma.aux import F, N


class TestSymClear(unittest.TestCase):
    """Sanity-test symbol life-cycle assumptions."""

    @classmethod
    def tearDownClass(cls):
        gamma.clear_gamma()

    def test_sym_clear_and_reset(self):
        """Clear and reset the same symbol.

        The length of _gamma shouldn't change.

        """

        self.assertEqual(0, len(gamma._gamma))

        x_idx = gamma.sym_declare("x")
        self.assertEqual(1, len(gamma._gamma))

        gamma.sym_set("x", F(N(0)))

        # len(_gamma) shouldn't change from 1, just because we cleared
        # a symbol.
        gamma.sym_clear(x_idx)
        self.assertEqual(1, len(gamma._gamma))

        what = gamma.sym_get(x_idx)
        assert what is not None

        self.assertEqual("x", what.label)
        self.assertEqual(Empty(), what.ast)

        # Try redeclaring "x"; the new and former indices should be
        # equal.
        x_idx_2 = gamma.sym_declare("x")
        self.assertEqual(x_idx, x_idx_2)

        # Now try setting "x" to a new value.
        gamma.sym_set("x", F(F(N(0))))

        what = gamma.sym_get(x_idx)
        assert what is not None

        self.assertEqual("x", what.label)
        self.assertEqual(F(F(N(0))), what.ast)

        # At the end of this, I should only have one definition inside
        # _gamma.
        self.assertEqual(1, len(gamma._gamma))
