import unittest

import lbd.beta as beta
from tests.core.aux import A, F, N

identity = F(N(0, 1))
self_apply = F(A(N(0, 1), N(0, 1)))

# I want to call this simply "apply", but Python has already taken the
# name.
applyfn = F(F(A(N(1, 2), N(0, 2))))

select_first = F(F(N(1, 2)))
select_second = F(F(N(0, 2)))
make_pair = F(F(F(A(A(N(0, 3),
                      N(2, 3)),
                    N(1, 3)))))


class TestBetaReduction(unittest.TestCase):
    def test_identity(self):
        term = A(identity, self_apply)

        reduced_term = beta.beta_reduce(term)

        self.assertEqual(reduced_term, self_apply)

    def test_2_10_example(self):
        term = A(F(A(N(0, 1), identity)),
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
        inner = F(F(A(N(1, 2), N(1, 2))))
        term = A(inner, inner)
        stop_point = F(A(inner, inner))

        self.term = term
        self.stop_point = stop_point

    def test_one_step(self):
        """Test one step in reducing stepwise-Ω."""

        actual = beta.beta_reduce(self.term)

        self.assertEqual(self.stop_point, actual)

    def test_two_steps(self):
        """Test two steps in reducing stepwise-Ω."""

        result1 = beta.beta_reduce(self.term)
        result2 = beta.beta_reduce(A(result1, identity))

        self.assertEqual(self.stop_point, result2)

    def test_many_steps(self):
        """Test many steps in reducing stepwise-Ω."""

        current = beta.beta_reduce(self.term)

        for _ in range(100):
            intermediate = beta.beta_reduce(current)
            current = beta.beta_reduce(A(intermediate, identity))

        self.assertEqual(self.stop_point, current)
