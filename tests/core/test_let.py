import unittest

from lbd.error import LambdaError
from lbd.evaluate import eval_raw_term
from tests.core.aux import IDENTITY


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
