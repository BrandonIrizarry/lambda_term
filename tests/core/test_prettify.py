import re
import unittest

import tests.core.aux as aux
from lbd.prettify import prettify


class TestPrettify(unittest.TestCase):
    """Test prettification of lambda terms without any free symbols."""

    def test_identity(self):
        """Test prettified identity function."""

        pretty_id = prettify(aux.IDENTITY)

        mobj = re.fullmatch(r"\\(\w+)\.\1", pretty_id)

        self.assertIsNotNone(mobj)

    def test_selectors(self):
        """Test 'select_first', 'select_second', and 'select_third'."""

        for i, sel in enumerate(aux.TRIPLE_SELECTORS):
            pretty = prettify(sel)

            mobj = re.fullmatch(
                rf"\\(\w+)\.\\(\w+)\.\\(\w+)\.\{i + 1}", pretty)

            self.assertIsNotNone(mobj)
