import unittest

import lbd.error as err
import lbd.evaluate as evl
import lbd.gamma as g
import lbd.tokenize as tkz
from lbd.error import LambdaError
from tests.gamma.aux import A, F, G, N, S


class TestAssignmentBasics(unittest.TestCase):
    def tearDown(self):
        g.clear_gamma()

    def test_top_level_assignment(self):
        term = "<x := \\x.x>"

        ast = evl.eval_raw_term(term)

        x_index = g.gamma("x")

        assert x_index is not None

        identity = F(N(0))

        # Check that we have the correct AST.
        self.assertEqual(ast, identity)

        # Check that \x.x has been assigned to the free name 'x'.
        sym = g.sym_get(x_index)

        assert sym is not None

        self.assertEqual(sym.label, "x")
        self.assertEqual(sym.ast, identity)

    def test_repeated_assignment(self):
        """Test that a free name can be redefined."""

        program = [
            "<a := \\x.x>; <b := \\x.x>",
            "(a b)",
            "<a := \\x.\\y.x>",
            "(a a b)",
            "<a := \\x.\\y.y>",
            "(a a b)",
        ]

        ast = None

        for line in program:
            tokens = tkz.tokenize(line)
            assert not isinstance(tokens, LambdaError)

            ast = evl.eval_line(tokens)
            assert not isinstance(ast, LambdaError)

        self.assertEqual(F(N(0)), ast)

    def test_inner_assignment(self):
        terms = [
            "<a := \\x.x>",
            "<b := \\f.\\a.(f a)>",
            "<c := \\x.\\y.y>",
            "(<select_first := \\x.\\y.x> c a)",
            "(select_first a b)",
        ]

        ast = None
        identity = F(N(0))

        for t in terms:
            ast = evl.eval_raw_term(t)
            self.assertNotIsInstance(ast, err.LambdaError)

        self.assertEqual(ast, identity)

    def test_nested_assignment(self):
        """Perform assignments that then get used later in the same
        reduction.

        """

        term = "(<first := \\x.\\y.x> <second := \\x.\\y.y>)"
        ast = evl.eval_raw_term(term)

        self.assertNotIsInstance(ast, err.LambdaError)
        second_index = g.gamma("second")

        assert second_index is not None

        # Let this variable stand for the AST we _know_ to be the
        # canonical value of second, for convenience.
        #
        # It hasn't been assigned yet in gamma, though, which is
        # partly the point of this test.
        SECOND = F(F(N(0)))

        expected = F(S(G(second_index, 1), SECOND))
        self.assertEqual(ast, expected)

    def test_delayed_assignment(self):
        """Make sure that abstraction delays an assignment."""

        term = "\\x.<foo := \\x.\\y.x>; foo"
        tokens = tkz.tokenize(term)
        assert not isinstance(tokens, LambdaError)

        self.assertRaises(ValueError, evl.eval_line, tokens)


class TestDepth(unittest.TestCase):
    """Test the depth field in name-ASTs.

    Mainly, we want to see if free symbols keep their indices into
    gamma consistent after beta-reduction, as well as to simply check
    if a given lambda term with free symbols parses correctly.

    """

    def tearDown(self):
        g.clear_gamma()

    def test_parse(self):
        decl = "<x := \\x.x>; <y := \\x.x>"
        term = "(\\u.\\v.(u x) y)"

        # Populate gamma.
        tokens = tkz.tokenize(decl)
        assert not isinstance(tokens, LambdaError)

        evl.eval_line(tokens)

        # Evaluate the main term here.
        ast = evl.eval_raw_term(term)

        x_index = g.gamma("x")
        y_index = g.gamma("y")

        self.assertEqual(x_index, 0)
        self.assertEqual(y_index, 1)

        assert x_index is not None
        assert y_index is not None

        self.assertEqual(ast, F(A(G(y_index, 1),
                                  G(x_index, 1))))


class TestAssignmentParameters(unittest.TestCase):
    """*** Test assignment parameters."""

    def tearDown(self):
        g.clear_gamma()

    def test_identity(self):
        term = "<identity x := x>"

        ast = evl.eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(ast, F(N(0)))

    def test_apply(self):
        term = "<apply f a := (f a)>"

        ast = evl.eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(ast, F(F(A(N(1),
                                    N(0)))))

    def test_if(self):
        term = "<if cond e1 e2 := (cond e1 e2)>"

        ast = evl.eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(ast, F(F(F(A(A(N(2),
                                        N(1)),
                                      N(0))))))
