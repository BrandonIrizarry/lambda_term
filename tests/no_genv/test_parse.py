import unittest

import lbd.desugar as dsg
import lbd.parse as parse
import lbd.term as term
import lbd.tokenize_lambda as tkz

A = term.new_application
F = term.new_abstraction
N = term.new_name


def parse_raw(raw_term: str) -> tuple[term.AST, int]:
    tokens = tkz.tokenize(raw_term)

    if isinstance(tokens, Exception):
        raise ValueError

    _tokens = dsg.desugar_def(tokens)

    if isinstance(_tokens, Exception):
        raise ValueError

    # For these tests, we don't need the def label, since there is
    # none here.
    tokens, _ = _tokens

    _ast = parse.parse_term(tokens, 0, [])

    if isinstance(_ast, Exception):
        raise ValueError

    ast, num_tokens = _ast

    return ast, num_tokens


class TestShorthand(unittest.TestCase):
    def test(self):
        ast = A(A(F(F(A(N(0),
                        N(1)))),
                  F(F(N(1)))),
                F(N(0)))

        ast_longhand = {'kind': 'application',
                        'left': {'kind': 'application',
                                 'left': {'body': {'body': {'kind': 'application',
                                                            'left': {'index': 0, 'kind': 'name'},
                                                            'right': {'index': 1, 'kind': 'name'}},
                                                   'kind': 'abstraction'},
                                          'kind': 'abstraction'},
                                 'right': {'body': {'body': {'index': 1, 'kind': 'name'},
                                                    'kind': 'abstraction'},
                                           'kind': 'abstraction'}},
                        'right': {'body': {'index': 0, 'kind': 'name'}, 'kind': 'abstraction'}}

        self.assertEqual(ast, ast_longhand)


class TestLegalTerms(unittest.TestCase):
    def test_2_2_a(self):
        raw_term = "   ((\\input.\\func.(  func input  ) \\first.\\second.first) \\sole.sole)"
        parsed, num_tokens = parse_raw(raw_term)

        ast = A(A(F(F(A(N(0),
                        N(1)))),
                  F(F(N(1)))),
                F(N(0)))

        self.assertEqual(parsed, ast)
        self.assertEqual(num_tokens, 25)

    def test_2_2_b(self):
        raw_term = "(((\\x.\\y.\\z.((x y) z) \\f.\\a.(f a)) \\i.i) \\j.j)"
        parsed, num_tokens = parse_raw(raw_term)

        ast = A(A(A(F(F(F(A(A(N(2),
                              N(1)),
                            N(0))))),
                    F(F((A(N(1),
                           N(0)))))),
                  F(N(0))),
                F(N(0)))

        self.assertEqual(parsed, ast)
        self.assertEqual(num_tokens, 40)

    def test_2_2_c(self):
        self.maxDiff = None
        raw_term = "(\\h.((\\a.\\f.(f a) h) h) \\f.(f f))"
        parsed, num_tokens = parse_raw(raw_term)

        ast = A(F(A(A(F(F(A(N(0),
                            N(1)))),
                      N(0)),
                    N(0))),
                F(A(N(0),
                    N(0))))

        self.assertEqual(parsed, ast)
        self.assertEqual(num_tokens, 28)


class TestIllegalTerms(unittest.TestCase):
    def test_term_incomplete(self):
        raw_term = "\\xy"

        with self.assertRaises(ValueError):
            parse_raw(raw_term)

        raw_term = "\\xylophone.(xylophone"

        with self.assertRaises(ValueError):
            parse_raw(raw_term)

    def test_abstraction_missing_dot(self):
        raw_term = "\\xy(x y)"

        with self.assertRaises(ValueError) as cm:
            parse_raw(raw_term)

    def test_application_no_opening_paren(self):
        raw_term = "\\x.\\y.x y)"

        with self.assertRaises(ValueError):
            parse_raw(raw_term)

    def test_abstraction_missing_keyword(self):
        raw_term = "x.x"

        with self.assertRaises(ValueError):
            parse_raw(raw_term)

    def test_extra_dots(self):
        raw_term = "\\x..x"

        with self.assertRaises(ValueError) as cm:
            parse_raw(raw_term)


class TestSugaredApplications(unittest.TestCase):
    def test_xyz(self):
        raw_term = "\\x.\\y.\\z.(x y z)"

        parsed, _, = parse_raw(raw_term)

        # Note how the generated AST includes the desugared extra
        # application.
        ast = F(F(F(A(A(N(2),
                        N(1)),
                      N(0)))))

        self.assertEqual(parsed, ast)

    def test_complex(self):
        raw_term = "\\false.\\iszero.\\n.((iszero n) n (n false))"

        parsed, _, = parse_raw(raw_term)

        ast = F(F(F(A(A(A(N(1),
                          N(0)),
                        N(0)),
                      A(N(0),
                        N(2))))))

        self.assertEqual(parsed, ast)
