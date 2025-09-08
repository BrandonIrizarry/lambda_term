import re
import unittest

import lbd.prettify as prettify
from tests.core.aux import A, F, N

identity = F(N(0))

selectors = {
    "first": F(F(F(N(2)))),
    "second": F(F(F(N(1)))),
    "third": F(F(F(N(0)))),
}


class TestPrettify(unittest.TestCase):
    """Test prettification of lambda terms without any free symbols."""

    def test_identity(self):
        """Test prettified identity function."""

        pretty_id, _ = prettify.prettify(identity, [], 0, False, set())

        mobj = re.fullmatch(r"\\(\w+)\.\1", pretty_id)

        self.assertIsNotNone(mobj)

    def test_selectors(self):
        """Test 'select_first', 'select_second', and 'select_third'."""

        for i, (ordinal, _) in enumerate(selectors.items()):
            pretty, _ = prettify.prettify(
                selectors[ordinal], [], 0, False, set())

            mobj = re.fullmatch(
                rf"\\(\w+)\.\\(\w+)\.\\(\w+)\.\{i + 1}", pretty)

            self.assertIsNotNone(mobj)


class TestUnused(unittest.TestCase):
    """Prettification of lambda terms involving unused local binders."""

    def test_unused_in_application(self):
        """Verify that argument is unused inside application."""

        term = F(F(F(A(N(1), N(2)))))
        pretty, _ = prettify.prettify(term, [], 0, False, set())

        mobj = re.fullmatch(r"\\(\w+)\.\\(\w+)\.\\_.\(\2\n\s+\1\)", pretty)

        self.assertIsNotNone(mobj)
