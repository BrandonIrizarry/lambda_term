import unittest

import lbd.error as err
import lbd.evaluate as evl
import lbd.gamma as g
from tests.aux import F, G, N, S


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

    def test_nested_assignment(self):
        """Perform assignments that then get used later in the same
        reduction.

        """

        decl = "sym first second"

        evl.eval_raw_term(decl)

        term = "(<first \\x.\\y.x> <second \\x.\\y.y>)"
        ast = evl.eval_raw_term(term)

        self.assertNotIsInstance(ast, err.LambdaError)
        second_index = g.gamma("second")

        assert second_index is not None

        # Let this variable stand for the AST we _know_ to be the
        # canonical value of second, for convenience.
        #
        # It hasn't been assigned yet in gamma, though, which is
        # partly the point of this test.
        SECOND = F(F(N(0, 2)))

        expected = F(S(G(second_index, 1), SECOND))
        self.assertEqual(ast, expected)

        g.clear_gamma()
