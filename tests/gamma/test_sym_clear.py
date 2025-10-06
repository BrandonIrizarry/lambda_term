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
        SYM_NAME = "martian"

        x_idx = gamma.sym_declare(SYM_NAME)
        self.assertEqual(1, len(gamma._gamma))

        gamma.sym_set(SYM_NAME, F(N(0, 1)))

        # len(_gamma) shouldn't change from 1, just because we cleared
        # a symbol.
        gamma.sym_clear(x_idx)
        self.assertEqual(1, len(gamma._gamma))

        what = gamma.sym_get(x_idx)
        assert what is not None

        self.assertEqual(SYM_NAME, what.label)
        self.assertEqual(Empty(), what.ast)

        # Try redeclaring SYM_NAME; the new and former indices should be
        # equal.
        x_idx_2 = gamma.sym_declare(SYM_NAME)
        self.assertEqual(x_idx, x_idx_2)

        # Now try setting SYM_NAME to a new value.
        gamma.sym_set(SYM_NAME, F(F(N(0, 2))))

        what = gamma.sym_get(x_idx)
        assert what is not None

        self.assertEqual(SYM_NAME, what.label)
        self.assertEqual(F(F(N(0, 2))), what.ast)

        # At the end of this, I should only have one definition inside
        # _gamma.
        self.assertEqual(1, len(gamma._gamma))
