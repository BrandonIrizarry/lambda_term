import re
import unittest

import lbd.repl as repl
import lbd.term as term

N = term.new_name
G = term.new_free_name
F = term.new_abstraction
A = term.new_application

identity = F(N(0, 1))


class TestPrettify(unittest.TestCase):
    def test_identity(self):
        """Test prettified identity function."""

        pretty_id = repl.prettify(identity, [])

        mobj = re.fullmatch(r"\\(\w+)\.\1", pretty_id)

        self.assertIsNotNone(mobj)
