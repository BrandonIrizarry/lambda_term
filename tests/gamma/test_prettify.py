import re
import unittest

import lbd.repl as repl
import lbd.term as term

N = term.new_name
G = term.new_free_name
F = term.new_abstraction
A = term.new_application

identity = F(N(0, 1))

selectors = {
    "first": F(F(F(N(2, 3)))),
    "second": F(F(F(N(1, 3)))),
    "third": F(F(F(N(0, 3)))),
}


class TestPrettify(unittest.TestCase):
    def test_identity(self):
        """Test prettified identity function."""

        pretty_id = repl.prettify(identity, [])

        mobj = re.fullmatch(r"\\(\w+)\.\1", pretty_id)

        self.assertIsNotNone(mobj)

    def test_selectors(self):
        """Test 'select_first', 'select_second', and 'select_third'."""

        for i, (ordinal, _) in enumerate(selectors.items()):
            pretty = repl.prettify(selectors[ordinal], [])
            mobj = re.fullmatch(
                rf"\\(\w+)\.\\(\w+)\.\\(\w+)\.\{i + 1}", pretty)

            self.assertIsNotNone(mobj)
