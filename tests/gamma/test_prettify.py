import re
import unittest

import lbd.repl as repl
import lbd.term as term

N = term.new_name
G = term.new_free_name
F = term.new_abstraction
A = term.new_application

identity = F(N(0, 1))
first = F(F(F(N(2, 3))))
second = F(F(F(N(1, 3))))
third = F(F(F(N(0, 3))))


class TestPrettify(unittest.TestCase):
    def test_identity(self):
        """Test prettified identity function."""

        pretty_id = repl.prettify(identity, [])

        mobj = re.fullmatch(r"\\(\w+)\.\1", pretty_id)

        self.assertIsNotNone(mobj)

    def test_first(self):
        """Test 'select_first'."""

        pretty_first = repl.prettify(first, [])

        mobj = re.fullmatch(r"\\(\w+)\.\\(\w+)\.\\(\w+)\.\1", pretty_first)

        self.assertIsNotNone(mobj)
