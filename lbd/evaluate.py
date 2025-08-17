import re
from typing import Any, TypedDict

import lbd.beta as beta
import lbd.directive as dtv
import lbd.error as err
import lbd.parse as parse
import lbd.tokenize_lambda as tkz


class GenvEntry(TypedDict):
    label: str
    ast: dict[str, Any]


type Genv = list[GenvEntry]


def eval_raw_term(raw_term: str, genv: Genv) -> dict[str, Any] | Exception:
    tokens = tkz.tokenize(raw_term)

    if isinstance(tokens, Exception):
        return tokens

    _parsed = parse.parse_term(tokens, 0, [])

    if isinstance(_parsed, Exception):
        return _parsed

    ast, num_tokens = _parsed

    # FIXME: right now I'm checking this _after_ desugaring, so at
    # some point I may need to disentangle this.
    if num_tokens < len(tokens):
        return err.error(tokens, num_tokens, err.Err.TRAILING_GARBAGE)

    return beta.beta_reduce(ast)


def eval_program(program: list[str], genv: Genv) -> dict[str, Any] | Exception:
    value = dict()

    for line in program:
        ast = eval_line(line, genv)

        if isinstance(ast, Exception):
            return ast

        value = ast

    return value


def eval_line(repl_input: str, genv: Genv) -> dict[str, Any] | Exception:
    """Given REPL_INPUT, either evaluate as a directive, or else a raw
    lambda term.

    """

    # Try to match the following pattern:
    #
    # NAME PARAMS...
    #
    # where NAME is the directive in question (e.g., "load").
    _directive = re.match(r"(\.)(?P<name>.+?\b)(?P<params>.*)", repl_input)

    if _directive is None:
        # The program is this single line.
        ast = eval_raw_term(repl_input, genv)

        if isinstance(ast, Exception):
            return ast

        return ast

    name = _directive.group("name")
    params = _directive.group("params").strip().split(" ")

    # FIXME: right now, this just assumes that the directive
    # always returns a program as the user_data field.
    program = dtv.eval_directive(name, params)

    if isinstance(program, Exception):
        return program

    value = eval_program(program, genv)

    if isinstance(value, Exception):
        return value

    return value
