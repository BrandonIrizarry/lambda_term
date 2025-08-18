import unittest

import lbd.error as err
import lbd.parse as parse
import lbd.term as term
import lbd.tokenize_lambda as tkz

A = term.new_application
F = term.new_abstraction
N = term.new_name


def parse_raw(raw_term: str) -> tuple[term.AST, int] | Exception:
    tokens = tkz.tokenize(raw_term)

    if isinstance(tokens, Exception):
        return tokens

    _ast = parse.parse_term(tokens, 0, [])

    if isinstance(_ast, Exception):
        return _ast

    ast, num_tokens = _ast

    if num_tokens < len(tokens):
        return err.error(tokens, num_tokens, err.Err.TRAILING_GARBAGE)

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
        _parsed = parse_raw(raw_term)

        if not isinstance(_parsed, Exception):
            parsed, num_tokens = _parsed

            ast = A(A(F(F(A(N(0),
                            N(1)))),
                      F(F(N(1)))),
                    F(N(0)))

            self.assertEqual(parsed, ast)
            self.assertEqual(num_tokens, 25)
        else:
            # Unfortunately, this otherwise can't perform type
            # narrowing. So we have to synthesize the case where the
            # test fails if there's an Exception.
            self.assertNotIsInstance(_parsed, Exception)

    def test_2_2_b(self):
        raw_term = "(((\\x.\\y.\\z.((x y) z) \\f.\\a.(f a)) \\i.i) \\j.j)"
        _parsed = parse_raw(raw_term)

        if not isinstance(_parsed, Exception):
            parsed, num_tokens = _parsed

            ast = A(A(A(F(F(F(A(A(N(2),
                                  N(1)),
                                N(0))))),
                        F(F((A(N(1),
                               N(0)))))),
                      F(N(0))),
                    F(N(0)))

            self.assertEqual(parsed, ast)
            self.assertEqual(num_tokens, 40)
        else:
            self.assertNotIsInstance(_parsed, Exception)

    def test_2_2_c(self):
        self.maxDiff = None
        raw_term = "(\\h.((\\a.\\f.(f a) h) h) \\f.(f f))"
        _parsed = parse_raw(raw_term)

        if not isinstance(_parsed, Exception):
            parsed, num_tokens = _parsed

            ast = A(F(A(A(F(F(A(N(0),
                                N(1)))),
                          N(0)),
                        N(0))),
                    F(A(N(0),
                        N(0))))

            self.assertEqual(parsed, ast)
            self.assertEqual(num_tokens, 28)
        else:
            self.assertNotIsInstance(_parsed, Exception)


class TestIllegalTerms(unittest.TestCase):
    def test_term_incomplete(self):
        raw_term = "\\xy"

        exception = parse_raw(raw_term)

        if isinstance(exception, err.LambdaError):
            self.assertEqual(exception.kind, err.Err.INCOMPLETE)
        else:
            self.assertIsInstance(exception, err.LambdaError)

        raw_term = "\\xylophone.(xylophone"

        exception = parse_raw(raw_term)

        if isinstance(exception, err.LambdaError):
            self.assertEqual(exception.kind, err.Err.INCOMPLETE)
        else:
            self.assertIsInstance(exception, err.LambdaError)

    def test_abstraction_missing_dot(self):
        raw_term = "\\xy(x y)"

        exception = parse_raw(raw_term)

        if isinstance(exception, err.LambdaError):
            self.assertEqual(exception.kind, err.Err.MISSING_DOT)
        else:
            self.assertIsInstance(exception, err.LambdaError)

    def test_application_no_opening_paren(self):
        raw_term = "\\x.\\y.x y)"

        exception = parse_raw(raw_term)

        if isinstance(exception, err.LambdaError):
            self.assertEqual(exception.kind, err.Err.TRAILING_GARBAGE)
        else:
            self.assertIsInstance(exception, err.LambdaError)

    def test_abstraction_missing_keyword(self):
        raw_term = "x.x"

        exception = parse_raw(raw_term)

        # Before, this raw_term was invalid because 'x' was parsed as
        # a name, and so the '.x' counted as trailing garbage (because
        # no valid token is present to spur on the parsing process.)
        # Now, it's invalid simply because the lack of the lambda
        # keyword means there's no longer a local binding for x,
        # meaning that it's an undeclared free symbol.
        if isinstance(exception, err.LambdaError):
            self.assertEqual(exception.kind, err.Err.UNDECLARED_SYMBOL)
        else:
            self.assertIsInstance(exception, err.LambdaError)

    def test_extra_dots(self):
        raw_term = "\\x..x"

        exception = parse_raw(raw_term)

        if isinstance(exception, err.LambdaError):
            self.assertEqual(exception.kind, err.Err.MEANINGLESS)
        else:
            self.assertIsInstance(exception, err.LambdaError)


class TestSugaredApplications(unittest.TestCase):
    def test_xyz(self):
        raw_term = "\\x.\\y.\\z.(x y z)"

        _parsed = parse_raw(raw_term)

        if not isinstance(_parsed, Exception):
            parsed, _ = _parsed

            # Note how the generated AST includes the desugared extra
            # application.
            ast = F(F(F(A(A(N(2),
                            N(1)),
                          N(0)))))

            self.assertEqual(parsed, ast)
        else:
            self.assertNotIsInstance(_parsed, Exception)

    def test_complex(self):
        raw_term = "\\false.\\iszero.\\n.((iszero n) n (n false))"

        _parsed = parse_raw(raw_term)

        if not isinstance(_parsed, Exception):
            parsed, _ = _parsed

            ast = F(F(F(A(A(A(N(1),
                              N(0)),
                            N(0)),
                          A(N(0),
                            N(2))))))

            self.assertEqual(parsed, ast)
        else:
            self.assertNotIsInstance(_parsed, Exception)
