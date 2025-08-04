import unittest

import beta
import error as err
import parse

A = beta.new_application
F = beta.new_abstraction
N = beta.new_name

identity = F(N(0))
applyfn = F(F(A(N(1), N(0))))
select_first = F(F(N(1)))
select_second = F(F(N(0)))


def evaluate(raw_term):
    """Perform evaluation of a user-supplied lambda term from start to
    finish.

    """

    ast, _ = parse.parse(raw_term)
    return beta.beta_reduce(ast)


class TestPersistentPrograms(unittest.TestCase):
    def test_small_program(self):
        prelude = [
            "def identity := \\x.x",
            "def apply fn arg := (fn arg)",
            "def select_first x y := x",
            "def select_second x y := y"
        ]

        for line in prelude:
            evaluate(line)

        raw_term_1 = "(select_first identity apply)"
        value_1 = evaluate(raw_term_1)

        self.assertEqual(value_1, identity)

        raw_term_2 = "(select_second identity apply)"
        value_2 = evaluate(raw_term_2)

        self.assertEqual(value_2, applyfn)

    def test_missing_definition(self):
        raw_term = "(select_first identity apply)"

        with self.assertRaises(err.UnboundNameError):
            evaluate(raw_term)
