import enum
import re
from typing import TypedDict

import lbd.error as err

IDENT = r"[A-Za-z_]\w*"


class Tk(enum.Enum):
    ASSIGN = enum.auto()
    NAME = enum.auto()
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    DOT = enum.auto()
    LAMBDA = enum.auto()
    DEF = enum.auto()


class Token(TypedDict):
    kind: Tk
    str: str


def assign_t() -> Token:
    """Return a new assign-token."""

    return {"kind": Tk.ASSIGN, "str": ":="}


def name_t(value) -> Token:
    """Return a new name-token."""

    return {"kind": Tk.NAME, "str": value}


def left_paren_t() -> Token:
    """Return a new left-paren-token."""

    return {"kind": Tk.LEFT_PAREN, "str": "("}


def right_paren_t() -> Token:
    """Return a new right-paren-token."""

    return {"kind": Tk.RIGHT_PAREN, "str": ")"}


def dot_t() -> Token:
    """Return a new dot-token."""

    return {"kind": Tk.DOT, "str": "."}


def lambda_t() -> Token:
    """Return a new lambda-token."""

    return {"kind": Tk.LAMBDA, "str": "\\"}


def def_t() -> Token:
    """Return a new def-token."""

    return {"kind": Tk.DEF, "str": "def"}


def is_name_t(token: Token) -> bool:
    """Return whether TOKEN is a name-token."""

    return token["kind"] == Tk.NAME


def is_lambda_t(token: Token) -> bool:
    """Return whether TOKEN is a lambda-token."""

    return token == lambda_t()


def is_left_paren_t(token: Token) -> bool:
    """Return whether TOKEN is a left-paren-token."""

    return token == left_paren_t()


def is_right_paren_t(token: Token) -> bool:
    """Return whether TOKEN is a right-paren-token."""

    return token == right_paren_t()


def is_dot_t(token: Token) -> bool:
    """Return whether TOKEN is a dot."""

    return token == dot_t()


def is_def_t(token: Token) -> bool:
    """Return whether TOKEN is the 'def' keyword."""

    return token == def_t()


def find(tokens: list[Token], token: Token) -> int:
    """Return the first index where TOKEN is found in TOKENS.

    If not found, return -1.

    """

    for i in range(len(tokens)):
        if tokens[i] == token:
            return i

    return -1


def tokenize(raw_term: str) -> list[Token] | Exception:
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
    tokens: list[Token] = []

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
                return err.IllegalTokenError(i, value)

        i += 1

    return tokens
