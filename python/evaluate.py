import typing

import beta
import error as err
import parse


class GenvEntry(typing.TypedDict):
    label: str
    ast: dict[typing.Any, typing.Any]


type Genv = list[GenvEntry]


def eval_raw_term(raw_term: str, genv: Genv):
    ast, _, label = parse.parse(raw_term, genv)

    # If we parsed a def-statement, associate the label with the
    # AST.
    if label is not None:
        genv.append({"label": label, "ast": ast})
        return ast

    return beta.beta_reduce(ast)


def eval_program(program: list[str], genv: Genv) -> dict[typing.Any, typing.Any]:
    value = None

    for line in program:
        try:
            value = eval_raw_term(line, genv)
        except (err.IllegalTokenError, err.ParseError) as e:
            print(e)
            return

    return value
