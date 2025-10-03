import unittest

import lbd.evaluate as evl
import lbd.gamma as g
from lbd.error import LambdaError
from lbd.term import bind
from tests.gamma.aux import A, N


class TestBind(unittest.TestCase):
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

    def test_bind(self):
        # An easy way to get the AST for 'succ'.
        succ = evl.eval_raw_term("succ")
        assert not isinstance(succ, LambdaError)

        bound = bind("false", succ)

        expected = evl.eval_raw_term("\\false.\\n.\\s.(s false n)")
        assert not isinstance(expected, LambdaError)

        self.assertEqual(expected, bound)

    def test_letrec(self):
        div1_raw = "let div1 x y := (if (greater y x) zero (succ (div1 (sub x y) y))) in div1"

        div1 = evl.eval_raw_term(div1_raw)
        assert not isinstance(div1, LambdaError)

        bound = bind("div1", div1)

        expected = evl.eval_raw_term(
            "\\div1.\\x.\\y.(if (greater y x) zero (succ (div1 (sub x y) y)))")
        assert not isinstance(expected, LambdaError)

        self.assertEqual(expected, bound)

    def test_bind_over_application(self):
        # Reuse some stuff in the prelude for simplicity.  We can't
        # use 'eval_raw_term' directly since it will evaluate any
        # non-assigned global symbols as 'nil', which isn't what we
        # want here.
        idx_one = g.gamma("one")
        assert idx_one is not None

        idx_two = g.gamma("two")
        assert idx_two is not None

        applyfn_unbound = A(N(idx_one, 0), N(idx_two, 0))
        assert not isinstance(applyfn_unbound, LambdaError)

        inner = bind("two", applyfn_unbound)
        applyfn = bind("one", inner)

        expected = evl.eval_raw_term("\\f.\\a.(f a)")
        assert not isinstance(expected, LambdaError)

        self.assertEqual(expected, applyfn)
