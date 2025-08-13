import unittest

import configuration as cfg
import directive as dtv
import evaluate as evl
import term

N = term.new_name
F = term.new_abstraction
A = term.new_application

zero = F(N(0))


class TestLoad(unittest.TestCase):
    def test_load_prelude(self):
        srcfile = cfg.lambda_filename("prelude")

        status = dtv.eval_directive("load", [srcfile])

        self.assertIsNone(status["error"])

        program = status["user_data"]

        self.assertEqual(len(program), 13)

    def test_load_inside_code_file(self):
        srcfile = cfg.lambda_filename("prelude_plus_mz")

        status = dtv.eval_directive("load", [srcfile])

        self.assertIsNone(status["error"])

        program = status["user_data"]

        status = evl.eval_program(program, [])

        self.assertIsNone(status["error"])

        self.assertEqual(status["user_data"], zero)
