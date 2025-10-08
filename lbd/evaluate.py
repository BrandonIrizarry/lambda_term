import lbd.beta as beta
import lbd.error as err
import lbd.gamma as g
import lbd.parse as parse
import lbd.term as term
import lbd.tokenize as tkz
from lbd.error import LambdaError
from lbd.prettify import prettify


def eval_raw_term(raw_term: str) -> term.AST | LambdaError:
    tokens = tkz.tokenize(raw_term)

    if isinstance(tokens, LambdaError):
        return tokens

    return eval_tokens(tokens)


def eval_tokens(tokens: list[tkz.Token]) -> term.AST | err.LambdaError:
    """A shortcut to get an AST right away from some tokens."""

    _parsed = parse.parse_term(tokens, 0, [])

    if isinstance(_parsed, err.LambdaError):
        return _parsed

    ast, num_tokens = _parsed

    if num_tokens < len(tokens):
        return err.error(tokens, num_tokens, err.Err.TRAILING_GARBAGE)

    result = beta.beta_reduce(ast)

    if isinstance(result, term.Name):
        index = result.index
        sym = g.sym_get(index)

        if sym is not None and sym.label.startswith("__"):
            print("INPUT: ", [str(t) for t in tokens])
            print("RESULT: ", prettify(result))

    beta.unwrap_cached_refs(result)

    # g.sym_clear_thunks("__")

    # return unwrapped
    return result
