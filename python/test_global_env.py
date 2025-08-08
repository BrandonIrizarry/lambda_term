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


class TestPreludeEnv(unittest.TestCase):
    prelude = [
        "def identity := \\x.x",
        "def apply fn arg := (fn arg)",
        "def select_first x y := x",
        "def select_second x y := y"
    ]

    def setUp(self):
        self.penv = program_env.ProgramEnv()
        self.penv.load_program(self.prelude)

    @unittest.expectedFailure
    def test_prelude_env(self):
        self.penv.run()
        genv = {
            "identity": F(N(0)),
            "apply": F(F(A(N(1), N(0)))),
            "select_first": F(F(N(1))),
            "select_second": F(F(N(0))),
        }

        self.assertEqual(self.penv.env, genv)


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


class TestMissingDefinitions(unittest.TestCase):
    def setUp(self):
        self.penv = program_env.ProgramEnv()

    def test_missing_definition(self):
        self.penv.append_line("(select_first identity apply)")

        with self.assertRaises(err.UnboundNameError):
            self.penv.run()


class TestClobberGlobal(unittest.TestCase):
    prelude = [
        "def id x := x",
        "def apply fn arg := (fn arg)",

        # The global 'id' is being shadowed here
        "def select_first id y := id"
    ]

    def setUp(self):
        self.penv = program_env.ProgramEnv()
        self.penv.load_program(self.prelude)

    @unittest.expectedFailure
    def test_env_substitution(self):
        self.penv.append_line("(select_first apply id)")
        value = self.penv.run()

        self.assertTrue("id" in self.penv.env)
        self.assertEqual(value, applyfn)


class TestRedefineGlobal(unittest.TestCase):
    prelude = [
        "def select_first x y := x",
        "def select_first x y := y",
        "def apply f n := (f n)"
    ]

    def setUp(self):
        self.penv = program_env.ProgramEnv()
        self.penv.load_program(self.prelude)

    def test_redefine_global(self):
        self.penv.append_line("(select_first select_first apply)")
        value = self.penv.run()

        self.assertEqual(value, applyfn)
