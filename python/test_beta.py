import unittest

from beta import *

A = new_application
F = new_abstraction
N = new_name

identity = F(N(0))
self_apply = F(A(N(0), N(0)))

# I want to call this simply "apply", but Python has already taken the
# name.
apply_fn = F(F(A(N(1), N(0))))


class TestBetaReduction(unittest.TestCase):
    def test_identity(self):
        term = A(identity, self_apply)

        reduced_term = beta_reduce(term)

        self.assertEqual(reduced_term, self_apply)

    def test_2_10_example(self):
        term = A(F(A(N(0), identity)),
                 self_apply)

        reduced_term = beta_reduce(term)

        self.assertEqual(reduced_term, identity)
