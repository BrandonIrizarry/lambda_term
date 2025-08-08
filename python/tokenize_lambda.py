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
    DEF = enum.auto()


def assign_t():
    """Return a new assign-token."""

    return {"kind": Token.ASSIGN, "str": ":="}


def name_t(value):
    """Return a new name-token."""

    return {"kind": Token.NAME, "value": value, "str": value}


def left_paren_t():
    """Return a new left-paren-token."""

    return {"kind": Token.LEFT_PAREN, "str": "("}


def right_paren_t():
    """Return a new right-paren-token."""

    return {"kind": Token.RIGHT_PAREN, "str": ")"}


def dot_t():
    """Return a new dot-token."""

    return {"kind": Token.DOT, "str": "."}


def lambda_t():
    """Return a new lambda-token."""

    return {"kind": Token.LAMBDA, "str": "\\"}


def def_t():
    """Return a new def-token."""

    return {"kind": Token.DEF, "str": "def"}


def is_name_t(token):
    """Return whether TOKEN is a name-token."""

    if "value" not in token:
        return False

    return token == name_t(token["value"])


def is_lambda_t(token):
    """Return whether TOKEN is a lambda-token."""

    return token == lambda_t()


def is_left_paren_t(token):
    """Return whether TOKEN is a left-paren-token."""

    return token == left_paren_t()


def is_right_paren_t(token):
    """Return whether TOKEN is a right-paren-token."""

    return token == right_paren_t()


def is_dot_t(token):
    """Return whether TOKEN is a dot."""

    return token == dot_t()


def is_def_t(token):
    """Return whether TOKEN is the 'def' keyword."""

    return token == def_t()


def find(tokens, token):
    """Return the first index where TOKEN is found in TOKENS.

    If not found, return -1.

    """

    for i in range(len(tokens)):
        if tokens[i] == token:
            return i

    return -1


def is_identifier(token):
    """Return True iff TOKEN is an identifier."""
    return re.fullmatch(IDENT, token)


def tokenize(raw_term: str):
    spec = [
        ("assign", ":="),
        ("def", r"def"),
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
                tokens.append(assign_t())
            case "def":
                tokens.append(def_t())
            case "name":
                tokens.append(name_t(value))
            case "left_paren":
                tokens.append(left_paren_t())
            case "right_paren":
                tokens.append(right_paren_t())
            case "dot":
                tokens.append(dot_t())
            case "lambda":
                tokens.append(lambda_t())
            case "space":
                continue
            case "error":
                raise err.IllegalTokenError(i, value)

        i += 1

    return tokens
