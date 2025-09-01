import unittest

import lbd.evaluate as evl
import lbd.gamma as g
import lbd.tokenize as tkz
from lbd.error import LambdaError


class TestNaturalNumbers(unittest.TestCase):
    def tearDown(self):
        g.clear_gamma()

    def test_basic_program(self):
        prelude = [
            "<zero := \\x.x>",
            "<first x y := x>; <true := first>",
            "<second x y := y>; <false := second>",
            "<iszero n := (n first)>",
            "<succ n := \\s.(s false n)>",
            "<if cond e1 e2 := (cond e1 e2)>",
            "<pred1 n := (n second)>",
            "<pred n := (if (iszero n) zero (pred1 n))>",
            "<one := (succ zero)>",
            "<two := (succ one)>",
            "<three := (succ two)>",
        ]

        for line in prelude:
            tokens = tkz.tokenize(line)
            assert not isinstance(tokens, LambdaError)

            ast = evl.eval_line(tokens)
            assert not isinstance(ast, LambdaError)

        one_pred = evl.eval_raw_term("(pred (pred three))")
        assert not isinstance(one_pred, LambdaError)

        one_simple = evl.eval_raw_term("one")
        assert not isinstance(one_simple, LambdaError)

        self.assertEqual(one_pred, one_simple)
