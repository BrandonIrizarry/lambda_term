import unittest

import lbd.error as err
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

    def test_inner_assignment(self):
        decl = "sym select_first a b c"

        evl.eval_raw_term(decl)

        terms = [
            "<a \\x.x>",
            "<b \\f.\\a.(f a)>",
            "<c \\x.\\y.y>",
            "(<select_first \\x.\\y.x> c a)",
            "(select_first a b)",
        ]

        ast = None
        identity = F(N(0, 1))

        for t in terms:
            ast = evl.eval_raw_term(t)
            self.assertNotIsInstance(ast, err.LambdaError)

        self.assertEqual(ast, identity)

        g.clear_gamma()
