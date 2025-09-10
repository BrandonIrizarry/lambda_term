import unittest

import lbd.evaluate as evl
import lbd.gamma as g
from lbd.error import LambdaError
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
