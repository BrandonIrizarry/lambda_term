import unittest

import error as err
import evaluate as evl
import term

A = term.new_application
F = term.new_abstraction
N = term.new_name

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

    def test_genv_after_prelude(self):
        expected: evl.Genv = [
            {"label": "identity", "ast": F(N(0))},
            {"label": "apply", "ast": F(F(A(N(1), N(0))))},
            {"label": "select_first", "ast": F(F(N(1)))},
            {"label": "select_second", "ast": F(F(N(0)))},
        ]

        actual: evl.Genv = []

        evl.eval_program(self.prelude, actual)

        self.assertEqual(actual, expected)


class TestSelectionCombinators(unittest.TestCase):
    prelude = [
        "def identity := \\x.x",
        "def apply fn arg := (fn arg)",
        "def select_first x y := x",
        "def select_second x y := y"
    ]

    def setUp(self):
        self.genv: evl.Genv = []
        evl.eval_program(self.prelude, self.genv)

    def test_select_first(self):
        term = "(select_first identity apply)"
        value = evl.eval_raw_term(term, self.genv)

        self.assertEqual(value, identity)

    def test_select_second(self):
        term = "(select_second identity apply)"
        value = evl.eval_raw_term(term, self.genv)

        self.assertEqual(value, applyfn)


class TestMissingDefinitions(unittest.TestCase):
    def test_missing_definition(self):
        with self.assertRaises(err.UnboundNameError):
            evl.eval_raw_term("(select_first identity apply)", [])


class TestClobberGlobal(unittest.TestCase):
    prelude = [
        "def id x := x",
        "def apply fn arg := (fn arg)",

        # The global 'id' is being shadowed here
        "def select_first id y := id"
    ]

    def setUp(self):
        self.genv: evl.Genv = []
        evl.eval_program(self.prelude, self.genv)

    def test_env_substitution(self):
        term = "(select_first apply id)"
        value = evl.eval_raw_term(term, self.genv)

        self.assertTrue({"label": "id", "ast": identity} in self.genv)
        self.assertEqual(value, applyfn)


class TestRedefineGlobal(unittest.TestCase):
    prelude = [
        "def select_first x y := x",
        "def select_first x y := y",
        "def apply f n := (f n)"
    ]

    def setUp(self):
        self.genv: evl.Genv = []
        evl.eval_program(self.prelude, self.genv)

    def test_redefine_global(self):
        term = "(select_first select_first apply)"
        value = evl.eval_raw_term(term, self.genv)

        self.assertEqual(value, applyfn)
