import unittest

from lbd.error import LambdaError
from lbd.evaluate import eval_raw_term
from tests.core.aux import FIRST, IDENTITY


class TestLet(unittest.TestCase):
    """Let expressions."""

    def test_nested_let(self):
        """Nested let expressions."""

        term = """
let first := \\x.\\y.x in
    let second := \\x.\\y.y in
        let id := \\x.x in
            (second second id)
"""

        ast = eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(IDENTITY, ast)

    def test_assignment_params(self):
        """Assignment params for let-expressions."""

        term = "let apply f a := (f a) in (apply \\x.x \\x.\\y.x)"
        ast = eval_raw_term(term)
        assert not isinstance(ast, LambdaError)

        self.assertEqual(FIRST, ast)
