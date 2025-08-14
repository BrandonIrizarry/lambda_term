import unittest

import lbd.configuration as cfg
import lbd.directive as dtv
import lbd.evaluate as evl
import lbd.term as term

N = term.new_name
F = term.new_abstraction
A = term.new_application

# Note that zero is defined using the identity function.
zero = F(N(0))


class TestMakeZero(unittest.TestCase):
    PRELUDE = cfg.lambda_filename("prelude")
    SRCFILE = cfg.lambda_filename("make_zero")

    def test_three(self):
        status = dtv.eval_directive("load", [self.PRELUDE])

        self.assertIsNone(status["error"])

        prelude_defs = status["user_data"]

        genv: evl.Genv = []

        evl.eval_program(prelude_defs, genv)

        status = dtv.eval_directive("load", [self.SRCFILE])

        self.assertIsNone(status["error"])

        main_program = status["user_data"]

        # Pass in the genv that was populated by the definitions found
        # in 'prelude.lbd'.
        status = evl.eval_program(main_program, genv)

        self.assertIsNone(status["error"])

        ast = status["user_data"]

        self.assertEqual(ast, zero)
