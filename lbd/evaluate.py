import re
import typing

import lbd.beta as beta
import lbd.desugar as dsg
import lbd.directive as dtv
import lbd.error as err
import lbd.parse as parse
import lbd.status as status
import lbd.tokenize_lambda as tkz


class GenvEntry(typing.TypedDict):
    label: str
    ast: dict[typing.Any, typing.Any]


type Genv = list[GenvEntry]


def eval_raw_term(raw_term: str, genv: Genv):
    tokens = tkz.tokenize(raw_term)
    err.ParseError.set_tokens(tokens)

    # FIXME: setting 'tokens' twice like this looks awkward. Was it
    # event the right thing to do?
    tokens, label = dsg.desugar_def(tokens[:])

    try:
        ast, num_tokens = parse.parse_term(tokens, 0, [])

        if num_tokens < len(tokens):
            raise err.TrailingGarbageError(num_tokens, tokens)

        # If we parsed a def-statement, associate the label with the
        # AST.
        if label is not None:
            genv.append({"label": label, "ast": ast})
            return ast

        return beta.beta_reduce(ast)
    except IndexError:
        raise err.IncompleteTermError(len(tokens), tokens)


def eval_program(program: list[str], genv: Genv) -> status.Status:
    value = dict()

    for line in program:
        try:
            status = eval_line(line, genv)

            if status["error"]:
                return status

            value = status["user_data"]
        except (err.IllegalTokenError, err.ParseError) as e:
            return {"user_data": None, "error": str(e)}

    return {"user_data": value, "error": None}


def eval_line(repl_input: str, genv: Genv) -> status.Status:
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

        return {"user_data": ast, "error": None}

    name = _directive.group("name")
    params = _directive.group("params").strip().split(" ")

    # FIXME: right now, this just assumes that the directive
    # always returns a program as the user_data field.
    status = dtv.eval_directive(name, params)

    if status["error"] is not None:
        return status

    program = status["user_data"]

    status = eval_program(program, genv)

    if status["error"]:
        return status

    return {"user_data": status["user_data"], "error": None}
