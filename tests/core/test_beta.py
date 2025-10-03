import unittest

import lbd.beta as beta
import tests.core.aux as aux
from tests.core.aux import A, F, N


class TestBetaReduction(unittest.TestCase):
    def test_identity(self):
        term = A(aux.IDENTITY, aux.SELF_APPLY)

        reduced_term = beta.beta_reduce(term)

        self.assertEqual(reduced_term, aux.SELF_APPLY)

    def test_2_10_example(self):
        term = A(F(A(N(0, 1), aux.IDENTITY)),
                 aux.SELF_APPLY)

        reduced_term = beta.beta_reduce(term)

        self.assertEqual(reduced_term, aux.IDENTITY)

    def test_pairing(self):
        pair_identity = beta.beta_reduce(A(aux.PAIR, aux.IDENTITY))
        pair_identity_applyfn = beta.beta_reduce(A(pair_identity, aux.APPLY))

        first = beta.beta_reduce(A(pair_identity_applyfn, aux.FIRST))
        self.assertEqual(first, aux.IDENTITY)

        second = beta.beta_reduce(A(pair_identity_applyfn, aux.SECOND))
        self.assertEqual(second, aux.APPLY)


class TestStepwiseOmega(unittest.TestCase):
    """Examine a stepwise version of Ω."""

    def setUp(self):
        inner = F(F(A(N(1, 3), N(1, 3))))
        term = A(inner, inner)
        stop_point = F(A(inner, inner))

        self.term = term
        self.stop_point = stop_point

    def test_one_step(self):
        """Test one step in reducing stepwise-Ω."""

        actual = beta.beta_reduce(self.term)

        self.assertEqual(self.stop_point, actual)

    def test_many_steps(self):
        """Test many steps in reducing stepwise-Ω."""

        current = beta.beta_reduce(self.term)

        for _ in range(100):
            intermediate = beta.beta_reduce(current)
            current = beta.beta_reduce(A(intermediate, aux.IDENTITY))

        self.assertEqual(self.stop_point, current)


class TestChapterTwoPointTwo(unittest.TestCase):
    """Based on beta-reduction exercises found in Section 2.2.

    The book is An Introduction to Programming Through Lambda
    Calculus, by Greg Michaelson (Dover, 2011)

    We skip part (c) because it's a trick question: the given
    expression evaluates to Ω.

    """

    def test_a(self):
        """Exercise 2.2, part (a)."""

        term = A(A(F(F(A(N(0, 2),
                         N(1, 2)))),
                   F(F(N(1, 2)))),
                 F(N(0, 1)))

        ast = beta.beta_reduce(term)

        self.assertEqual(aux.FIRST, ast)

    def test_b(self):
        """Exercise 2.2, part (b)."""

        term = A(A(A(F(F(F(A(A(N(2, 3),
                               N(1, 3)),
                             N(0, 3))))),
                     aux.APPLY),
                   aux.IDENTITY),
                 aux.IDENTITY)

        ast = beta.beta_reduce(term)

        self.assertEqual(aux.IDENTITY, ast)

    def test_d(self):
        """Exercise 2.2, part (d)."""

        term = A(A(aux.APPLY,
                   A(aux.IDENTITY,
                     aux.FIRST)),
                 aux.IDENTITY)

        ast = beta.beta_reduce(term)

        self.assertEqual(aux.SECOND, ast)

    def test_e(self):
        """Exercise 2.2, part (e)."""

        term = A(A(A(F(F(F(A(N(2, 3),
                             A(N(1, 3),
                               N(0, 3)))))),
                     aux.SELF_APPLY),
                   aux.SECOND),
                 aux.FIRST)

        ast = beta.beta_reduce(term)

        self.assertEqual(aux.IDENTITY, ast)
