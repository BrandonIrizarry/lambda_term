import enum
import re

import error as err

IDENT = r"[A-Za-z_]\w*"


class Token(enum.Enum):
    ASSIGN = enum.auto()
    NAME = enum.auto()
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    DOT = enum.auto()
    LAMBDA = enum.auto()


def is_identifier(token):
    """Return True iff TOKEN is an identifier."""
    return re.fullmatch(IDENT, token)


def tokenize(raw_term: str):
    spec = [
        ("assign", ":="),
        ("name", IDENT),
        ("left_paren", r"\("),
        ("right_paren", r"\)"),
        ("dot", r"\."),
        ("lambda", r"\\"),
        ("space", r"[\t ]"),
        ("error", r".")
    ]

    pats = [f"(?P<{kind}>{pat})" for (kind, pat) in spec]
    token_pattern = "|".join(pats)
    tokens = []

    # Track the current iteration index, to make IllegalTokenError
    # consistent with other errors.
    i = 0
    for mobj in re.finditer(token_pattern, raw_term):
        kind = mobj.lastgroup

        if kind is None:
            raise ValueError("Fatal: found 'None'")

        value = mobj.group()

        match kind:
            case "assign":
                tokens.append({"kind": Token.ASSIGN})
            case "name":
                tokens.append({"kind": Token.NAME, "value": value})
            case "left_paren":
                tokens.append({"kind": Token.LEFT_PAREN})
            case "right_paren":
                tokens.append({"kind": Token.RIGHT_PAREN})
            case "dot":
                tokens.append({"kind": Token.DOT})
            case "lambda":
                tokens.append({"kind": Token.LAMBDA})
            case "space":
                continue
            case "error":
                raise err.IllegalTokenError(i, value)

        i += 1

    return tokens
