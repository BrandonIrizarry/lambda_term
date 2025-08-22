import lbd.beta as beta
import lbd.error as err
import lbd.gamma as g
import lbd.parse as parse
import lbd.term as term
import lbd.token_defs as tdef
import lbd.tokenize as tkz
from lbd.error import LambdaError


def eval_raw_term(raw_term: str) -> term.AST | LambdaError:
    tokens = tkz.tokenize(raw_term)

    if isinstance(tokens, LambdaError):
        return tokens

    # If the first token is SYM, scan the given list of names and add
    # them to gamma.
    match tokens[0]["kind"]:
        case tdef.Tk.SYM:
            last = 0

            for i, t in enumerate(tokens[1:], start=1):
                if t["kind"] != tdef.Tk.NAME:
                    return err.error(tokens, i, err.Err.INVALID_SYM_DECL)

                last = g.sym_declare(t["value"])

            return term.new_name(last)
        case _:
            _parsed = parse.parse_term(tokens, 0, [])

            if isinstance(_parsed, LambdaError):
                return _parsed

            ast, num_tokens = _parsed

            if num_tokens < len(tokens):
                return err.error(tokens, num_tokens, err.Err.TRAILING_GARBAGE)

            return beta.beta_reduce(ast)
