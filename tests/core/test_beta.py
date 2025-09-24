import unittest

import lbd.beta as beta
from tests.core.aux import A, F, N

identity = F(N(0))
self_apply = F(A(N(0), N(0)))

# I want to call this simply "apply", but Python has already taken the
# name.
applyfn = F(F(A(N(1), N(0))))

select_first = F(F(N(1)))
select_second = F(F(N(0)))
make_pair = F(F(F(A(A(N(0),
                      N(2)),
                    N(1)))))


class TestBetaReduction(unittest.TestCase):
    def test_identity(self):
        term = A(identity, self_apply)

        reduced_term = beta.beta_reduce(term)

        self.assertEqual(reduced_term, self_apply)

    def test_2_10_example(self):
        term = A(F(A(N(0), identity)),
                 self_apply)

        reduced_term = beta.beta_reduce(term)

        self.assertEqual(reduced_term, identity)

    def test_pairing(self):
        pair_identity = beta.beta_reduce(A(make_pair, identity))
        pair_identity_applyfn = beta.beta_reduce(A(pair_identity, applyfn))

        first = beta.beta_reduce(A(pair_identity_applyfn, select_first))
        self.assertEqual(first, identity)

        second = beta.beta_reduce(A(pair_identity_applyfn, select_second))
        self.assertEqual(second, applyfn)


class TestStepwiseOmega(unittest.TestCase):
    """Examine a stepwise version of Ω."""

    def setUp(self):
        inner = F(F(A(N(1), N(1))))
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
            current = beta.beta_reduce(A(intermediate, identity))

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

        term = A(A(F(F(A(N(0),
                         N(1)))),
                   F(F(N(1)))),
                 F(N(0)))

        ast = beta.beta_reduce(term)

        self.assertEqual(select_first, ast)

    def test_b(self):
        """Exercise 2.2, part (b)."""

        term = A(A(A(F(F(F(A(A(N(2),
                               N(1)),
                             N(0))))),
                     applyfn),
                   identity),
                 identity)

        ast = beta.beta_reduce(term)

        self.assertEqual(identity, ast)

    def test_d(self):
        """Exercise 2.2, part (d)."""

        term = A(A(applyfn,
                   A(identity,
                     select_first)),
                 identity)

        ast = beta.beta_reduce(term)

        self.assertEqual(select_second, ast)

    def test_e(self):
        """Exercise 2.2, part (e)."""

        term = A(A(A(F(F(F(A(N(2),
                             A(N(1),
                               N(0)))))),
                     self_apply),
                   select_second),
                 select_first)

        ast = beta.beta_reduce(term)

        self.assertEqual(identity, ast)
