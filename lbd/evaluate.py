import lbd.beta as beta
import lbd.error as err
import lbd.parse as parse
import lbd.term as term
import lbd.token_defs as tdef
import lbd.tokenize as tkz
from lbd.error import LambdaError


def eval_raw_term(raw_term: str) -> term.AST | LambdaError:
    tokens = tkz.tokenize(raw_term)

    if isinstance(tokens, LambdaError):
        return tokens

    return eval_tokens(tokens)


def eval_line(tokens: list[tkz.Token]) -> term.AST | LambdaError:
    """Evaluate a line.

    A line is one or more terms, where semicolon is the separator.

    """

    ast = None
    i = 0
    buf: list[tkz.Token] = []

    while i < len(tokens):
        t = tokens[i]
        kind = t.kind

        if kind != tdef.Tk.SEMICOLON:
            buf.append(t)

        else:
            ast = eval_tokens(buf)

            if isinstance(ast, err.LambdaError):
                return ast

            buf.clear()

        i += 1

    # If buf has elements, then the line has ended without a semicolon
    # (which is naturally allowed.) So we must therefore evaluate
    # what's left in buf.
    if len(buf) != 0:
        ast = eval_tokens(buf)

        if isinstance(ast, err.LambdaError):
            return ast

        buf.clear()

    assert ast is not None

    return ast


def eval_tokens(tokens: list[tkz.Token]) -> term.AST | err.LambdaError:
    """A shortcut to get an AST right away from some tokens."""

    _parsed = parse.parse_term(tokens, 0, [])

    if isinstance(_parsed, err.LambdaError):
        return _parsed

    ast, num_tokens = _parsed

    if num_tokens < len(tokens):
        return err.error(tokens, num_tokens, err.Err.TRAILING_GARBAGE)

    return beta.beta_reduce(ast)
