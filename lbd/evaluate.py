import lbd.beta as beta
import lbd.error as err
import lbd.parse as parse
import lbd.tokenize as tkz
from lbd.error import LambdaError
from lbd.term import AST


def eval_raw_term(raw_term: str) -> AST | LambdaError:
    tokens = tkz.tokenize(raw_term)

    if isinstance(tokens, LambdaError):
        return tokens

    _parsed = parse.parse_term(tokens, 0, [])

    if isinstance(_parsed, LambdaError):
        return _parsed

    ast, num_tokens = _parsed

    if num_tokens < len(tokens):
        return err.error(tokens, num_tokens, err.Err.TRAILING_GARBAGE)

    return beta.beta_reduce(ast)
