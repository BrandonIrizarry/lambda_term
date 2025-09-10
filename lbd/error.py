import enum
from dataclasses import dataclass

import lbd.tokenize as tkz


class Err(enum.StrEnum):
    ASSIGN_TO_LOCAL = "Cannot assign to local variable"
    ILLEGAL_TOKEN = "Illegal token"
    INCOMPLETE = "Incomplete term"
    INVALID_NAME = "Invalid name"
    INVALID_PARAM = "Invalid parameter name"
    INVALID_SYM_DECL = "Invalid free-variable declaration"
    MALFORMED_DEF = "Malformed def statement"
    MEANINGLESS = "Meaningless token"
    MISSING = "Missing token"
    MISSING_ASSIGN_OP = "Missing assignment operator"
    MISSING_DOT = "Missing dot after parameter name"
    MISSING_IN_OP = "Missing 'in'"
    MISSING_PARAM = "Missing parameter"
    TRAILING_GARBAGE = "Trailing garbage"
    UNASSIGNED = "Unassigned free symbol"
    UNSPECIFIED = "Unspecified error"


@dataclass
class LambdaError(Exception):
    kind: Err
    message: str

    def __str__(self):
        return self.message


TOKEN_JOIN = " "


def error(tokens: list["tkz.Token"], pos: int, kind: Err) -> LambdaError:
    """Report a parsing error."""

    what = f"Position {pos}: {kind.value}"

    # Create a simple "debug" view of the given tokens.
    view = []

    outside = True

    for i in range(len(tokens)):
        t_raw = tokens[i].value

        if i == pos:
            view.append(f"{{{t_raw}}}")
            outside = False
        else:
            view.append(t_raw)

    if outside:
        view.append("???")

    what += f"\n{TOKEN_JOIN.join(view)}"

    return LambdaError(kind, what)
