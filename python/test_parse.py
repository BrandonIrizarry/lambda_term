import unittest

import error as err
from parse import *

A = new_application
F = new_abstraction
N = new_name


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
        parsed, num_tokens = parse(raw_term)

        ast = A(A(F(F(A(N(0),
                        N(1)))),
                  F(F(N(1)))),
                F(N(0)))

        self.assertEqual(parsed, ast)
        self.assertEqual(num_tokens, 25)

    def test_2_2_b(self):
        raw_term = "(((\\x.\\y.\\z.((x y) z) \\f.\\a.(f a)) \\i.i) \\j.j)"
        parsed, num_tokens = parse(raw_term)

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
        parsed, num_tokens = parse(raw_term)

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

        with self.assertRaises(err.IncompleteTermError):
            parse(raw_term)

        raw_term = "\\xylophone.(xylophone"

        with self.assertRaises(err.IncompleteTermError):
            parse(raw_term)

    def test_abstraction_missing_dot(self):
        raw_term = "\\xy(x y)"

        with self.assertRaises(err.AbstractionNoDotError) as cm:
            parse(raw_term)

        self.assertEqual(cm.exception.position, 2)

    def test_application_no_opening_paren(self):
        raw_term = "\\x.\\y.x y)"

        with self.assertRaises(err.TrailingGarbageError):
            parse(raw_term)

    def test_abstraction_missing_keyword(self):
        raw_term = "x.x"

        with self.assertRaises(err.UnboundNameError):
            parse(raw_term)

    def test_extra_dots(self):
        raw_term = "\\x..x"

        with self.assertRaises(err.StrayTokenError) as cm:
            parse(raw_term)

        self.assertEqual(cm.exception.token, ".")
