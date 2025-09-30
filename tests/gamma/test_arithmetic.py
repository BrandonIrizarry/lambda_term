import unittest

import lbd.evaluate as evl
import lbd.gamma as g
from lbd.error import LambdaError
from lbd.term import AST
from tests.gamma.aux import F, N


class TestNaturalNumbers(unittest.TestCase):
    def setUp(self):
        prelude = [
            "def zero := \\x.x",
            "def first x y := x",
            "def true := first",
            "def second x y := y",
            "def false := second",
            "def iszero n := (n first)",
            "def succ n := \\s.(s false n)",
            "def if cond e1 e2 := (cond e1 e2)",
            "def pred1 n := (n second)",
            "def pred n := (if (iszero n) zero (pred1 n))",
            "def one := (succ zero)",
            "def two := (succ one)",
            "def three := (succ two)",
        ]

        for line in prelude:
            ast = evl.eval_raw_term(line)
            assert not isinstance(ast, LambdaError)

    def tearDown(self):
        g.clear_gamma()

    def test_basic_program(self):
        one_pred = evl.eval_raw_term("(pred (pred three))")
        assert not isinstance(one_pred, LambdaError)

        one_simple = evl.eval_raw_term("one")
        assert not isinstance(one_simple, LambdaError)

        self.assertEqual(one_pred, one_simple)

    def test_definition_stability(self):
        """Global definitions don't change after beta reduction.

        Here, multiple reductions are performed to ensure that.

        """

        expected = F(F(N(0)))

        for _ in range(100):
            term = "(one first)"
            ast = evl.eval_raw_term(term)

            self.assertEqual(expected, ast)

        # Perhaps redundant, but one often doesn't know where bugs
        # truly lie. :)
        for _ in range(100):
            term = "(iszero one)"

            ast = evl.eval_raw_term(term)
            self.assertEqual(expected, ast)


class TestOperations(unittest.TestCase):
    def setUp(self):
        prelude = [
            "def zero := \\x.x",
            "def first x y := x",
            "def true := first",
            "def second x y := y",
            "def false := second",
            "def iszero n := (n first)",
            "def succ n := \\s.(s false n)",
            "def if cond e1 e2 := (cond e1 e2)",
            "def pred1 n := (n second)",
            "def pred n := (if (iszero n) zero (pred1 n))",
            "def add x y := (if (iszero y) x (add (succ x) (pred y)))",
            "def sub x y := (if (iszero y) x (sub (pred x) (pred y)))",
            "def mult x y := (if (iszero y) zero (add x (mult x (pred y))))",
            "let abs_diff x y := (add (sub x y) (sub y x)) in def equal x y := (iszero (abs_diff x y))",
            "def greater x y := (not (iszero (sub x y)))",
            "def greater_or_equal x y := (iszero (sub y x))",
            "def less x y := (not (greater_or_equal x y))",
            "def less_or_equal x y := (not (greater x y))",
            "letrec div1 x y := (if (greater y x) zero (succ (div1 (sub x y) y))) in def div x y := (if (iszero y) zero (div1 x y))",
            "def sum n := (if (iszero n) zero (add n (sum (pred n))))",
            "def one := (succ zero)",
            "def two := (succ one)",
            "def three := (succ two)",
            "def four := (succ three)",
            "def five := (succ four)",
            "def six := (succ five)",
            "def seven := (succ six)",
            "def eight := (succ seven)",
        ]

        for line in prelude:
            ast = evl.eval_raw_term(line)
            assert not isinstance(ast, LambdaError)

        true = evl.eval_raw_term("true")
        assert not isinstance(true, LambdaError)
        self.true = true

        false = evl.eval_raw_term("false")
        assert not isinstance(false, LambdaError)
        self.false = false

    def tearDown(self):
        g.clear_gamma()

    def test_add(self):
        """Add two small numbers."""

        check = evl.eval_raw_term("(equal (add two three) five)")
        assert not isinstance(check, LambdaError)

        self.assertEqual(self.true, check)

    def test_false_add(self):
        """No false flags when adding two small numbers."""

        check = evl.eval_raw_term("(equal (add two three) six)")
        assert not isinstance(check, LambdaError)

        self.assertEqual(self.false, check)

    def test_sub(self):
        """Subtract two small numbers."""

        check = evl.eval_raw_term("(equal (sub five three) two)")
        assert not isinstance(check, LambdaError)

        self.assertEqual(self.true, check)

    def test_false_sub(self):
        """No false flags when subtracting two small numbers."""

        check = evl.eval_raw_term("(equal (sub five three) three)")
        assert not isinstance(check, LambdaError)

        self.assertEqual(self.false, check)

    def test_mult(self):
        "Multiply two small numbers."

        check = evl.eval_raw_term("(equal (mult two three) six)")
        assert not isinstance(check, LambdaError)

        self.assertEqual(self.true, check)

    def test_false_mult(self):
        "No false flags when multiplying two small numbers."

        check = evl.eval_raw_term("(equal (mult two three) five)")
        assert not isinstance(check, LambdaError)

        self.assertEqual(self.false, check)
