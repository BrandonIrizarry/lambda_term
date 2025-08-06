import unittest

import beta
import error as err
import parse
import program_env

A = beta.new_application
F = beta.new_abstraction
N = beta.new_name

identity = F(N(0))
applyfn = F(F(A(N(1), N(0))))
select_first = F(F(N(1)))
select_second = F(F(N(0)))


class TestSelectionCombinators(unittest.TestCase):
    prelude = [
        "def identity := \\x.x",
        "def apply fn arg := (fn arg)",
        "def select_first x y := x",
        "def select_second x y := y"
    ]

    def setUp(self):
        self.penv = program_env.ProgramEnv()
        self.penv.load_program(self.prelude)

    def test_select_first(self):
        self.penv.append_line("(select_first identity apply)")
        value = self.penv.run()

        self.assertEqual(value, identity)

    def test_select_second(self):
        self.penv.append_line("(select_second identity apply)")
        value = self.penv.run()

        self.assertEqual(value, applyfn)


# class TestPersistentPrograms(unittest.TestCase):
#       def test_missing_definition(self):
#         raw_term = "(select_first identity apply)"

#         with self.assertRaises(err.UnboundNameError):
#             evaluate(raw_term)

#     # This test is why I need to completely revamp how global
#     # variables are applied to the current expression.
#     @unittest.expectedFailure
#     def test_env_substitution(self):
#         prelude = [
#             "def id x := x",
#             "def apply fn arg := (fn arg)",

#             # The 'id' should be locally bound, effectively shadowing
#             # the global definition.
#             "def select_first id y := id"
#         ]

#         evaluate_prelude(prelude)

#         raw_term = "(select_first apply id)"
#         value = evaluate(raw_term)

#         self.assertEqual(value, applyfn)
