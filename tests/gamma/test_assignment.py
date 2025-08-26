import unittest

import lbd.evaluate as evl
import lbd.gamma as g
from tests.aux import F, N


class TestAssignment(unittest.TestCase):
    def test_top_level_assignment(self):
        decl = "sym x"
        term = "<x \\x.x>"

        evl.eval_raw_term(decl)
        ast = evl.eval_raw_term(term)

        x_index = g.gamma("x")

        assert x_index is not None

        identity = F(N(0, 1))

        # Check that we have the correct AST.
        self.assertEqual(ast, identity)

        # Check that \x.x has been assigned to the free name 'x'.
        sym = g.sym_get(x_index)

        assert sym is not None

        self.assertEqual(sym.label, "x")
        self.assertEqual(sym.ast, identity)

        g.clear_gamma()
