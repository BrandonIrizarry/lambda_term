import enum
from dataclasses import dataclass

import lbd.tokenize_lambda as tkz


class Err(enum.StrEnum):
    INCOMPLETE = "Incomplete term"
    MEANINGLESS = "Meaningless token"
    MISSING_PARAM = "Missing parameter"
    INVALID_PARAM = "Invalid parameter name"
    MISSING_DOT = "Missing dot after parameter name"
    TRAILING_GARBAGE = "Trailing garbage"


@dataclass
class LambdaError(Exception):
    kind: Err
    message: str

    def __str__(self):
        return self.message


def parsing(tokens: list[tkz.Token], pos: int, kind: Err) -> Exception:
    """Report a parsing error."""

    what = f"Position {pos}: {kind.value}"

    # Create a simple "debug" view of the given tokens.
    view = []

    outside = True

    for i in range(len(tokens)):
        t_raw = tokens[i]["str"]

        if i == pos:
            view.append(f"{{{t_raw}}}")
            outside = False
        else:
            view.append(t_raw)

    if outside:
        view.append("???")

    what += f"\n{''.join(view)}"

    return LambdaError(kind, what)
