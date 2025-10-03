import unittest

import lbd.error as err
import lbd.evaluate as evl
import lbd.gamma as g
import tests.gamma.aux as aux
from lbd.error import LambdaError
from tests.gamma.aux import A, E, F, G, N, S


class TestAssignmentBasics(unittest.TestCase):
    def tearDown(self):
        g.clear_gamma()

    def test_top_level_assignment(self):
        term = "def x := \\x.x"

        ast = evl.eval_raw_term(term)

        x_index = g.gamma("x")

        assert x_index is not None

        # Check that we have the correct AST.
        self.assertEqual(ast, aux.IDENTITY)

        # Check that \x.x has been assigned to the free name 'x'.
        sym = g.sym_get(x_index)

        assert sym is not None

        self.assertEqual(sym.label, "x")
        self.assertEqual(sym.ast, aux.IDENTITY)

    def test_repeated_assignment(self):
        """Test that a free name can be redefined."""

        program = [
            "def a := \\x.x",
            "def b := \\x.x",
            "(a b)",
            "def a := \\x.\\y.x",
            "(a a b)",
            "def a := \\x.\\y.y",
            "(a a b)",
        ]

        ast = None

        for line in program:
            ast = evl.eval_raw_term(line)
            assert not isinstance(ast, LambdaError)

        self.assertEqual(aux.IDENTITY, ast)

    def test_inner_assignment(self):
        terms = [
            "def a := \\x.x",
            "def b := \\f.\\a.(f a)",
            "def c := \\x.\\y.y",
            "(def select_first := \\x.\\y.x c a)",
            "(select_first a b)",
        ]

        ast = None

        for t in terms:
            ast = evl.eval_raw_term(t)
            self.assertNotIsInstance(ast, err.LambdaError)

        self.assertEqual(ast, aux.IDENTITY)

    def test_nested_assignment(self):
        """Perform assignments that then get used later in the same
        reduction.

        """

        term = "(def first := \\x.\\y.x def second := \\x.\\y.y)"
        ast = evl.eval_raw_term(term)

        self.assertNotIsInstance(ast, err.LambdaError)
        second_index = g.gamma("second")

        assert second_index is not None

        expected = F(S(G(second_index, 1), aux.SECOND))
        self.assertEqual(ast, expected)

    def test_delayed_assignment(self):
        """Make sure that abstraction delays an assignment."""

        term1 = "\\x.def foo := \\x.\\y.x"
        term2 = "foo"

        evl.eval_raw_term(term1)
        empty = evl.eval_raw_term(term2)
        assert not isinstance(empty, LambdaError)

        self.assertEqual(E(), empty)


class TestDepth(unittest.TestCase):
    """Test the depth field in name-ASTs.

    Mainly, we want to see if free symbols keep their indices into
    gamma consistent after beta-reduction, as well as to simply check
    if a given lambda term with free symbols parses correctly.

    """

    def tearDown(self):
        g.clear_gamma()

    def test_parse(self):
        decl1 = "def x := \\x.x"
        decl2 = "def y := \\x.x"
        term = "(\\u.\\v.(u x) y)"

        # Populate gamma.
        evl.eval_raw_term(decl1)
        evl.eval_raw_term(decl2)

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
        term = "def identity x := x"

        ast = evl.eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(ast, aux.IDENTITY)

    def test_apply(self):
        term = "def apply f a := (f a)"

        ast = evl.eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(ast, aux.APPLY)

    def test_if(self):
        term = "def if cond e1 e2 := (cond e1 e2)"

        ast = evl.eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(ast, F(F(F(A(A(N(2, 3),
                                        N(1, 3)),
                                      N(0, 3))))))

    def test_mixed(self):
        """Left-hand parameters and right-hand binders."""

        term = "def first x := \\_.x"
        ast = evl.eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(ast, F(F(N(1, 2))))
