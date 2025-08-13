import unittest

import directive as dtv
import evaluate as evl
import term

N = term.new_name
F = term.new_abstraction
A = term.new_application

# Note that zero is defined using the identity function.
zero = F(N(0))


class TestMakeZero(unittest.TestCase):
    def test_three(self):
        status = dtv.eval_directive("load", ["prelude"])

        self.assertIsNone(status["error"])

        prelude_defs = status["user_data"]

        genv: evl.Genv = []

        evl.eval_program(prelude_defs, genv)

        status = dtv.eval_directive("load", ["tests/make_zero"])

        self.assertIsNone(status["error"])

        main_program = status["user_data"]

        # Pass in the genv that was populated by the definitions found
        # in 'prelude.lbd'.
        value = evl.eval_program(main_program, genv)

        self.assertEqual(value, zero)
