import enum
import re

import lbd.error as err
from typing import TypedDict

IDENT = r"[A-Za-z_]\w*"


class Tk(enum.StrEnum):
    ASSIGN = enum.auto()
    NAME = enum.auto()
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    DOT = enum.auto()
    LAMBDA = enum.auto()
    DEF = enum.auto()
    SYM = enum.auto()
    SPACE = enum.auto()
    ERROR = enum.auto()


class Token(TypedDict):
    kind: Tk
    name: str
    value: str
    regex: str


def new_token(kind: Tk, value: str, regex: str | None = None) -> Token:
    if regex is None:
        regex = re.escape(value)

    return {
        "kind": kind,
        "name": kind.name.lower(),
        "value": value,
        "regex": regex
    }


def name_t(value: str):
    return new_token(Tk.NAME, value, IDENT)


def get(tokens: list[Token], pos: int) -> Token | None:
    """Return the token at position POS.

    If POS is out of range, then return None.

    """

    if pos < 0:
        raise ValueError(f"Fatal: negative token-buffer index {pos}")

    if pos >= len(tokens):
        return None

    return tokens[pos]


def find(tokens: list[Token], token: Token) -> int:
    """Return the first index where TOKEN is found in TOKENS.

    If not found, return -1.

    """

    for i in range(len(tokens)):
        if tokens[i] == token:
            return i

    return -1


# Note that the spec is order-sensitive, that is, "name" and "error"
# must remain in their positions at the bottom of this dict for regex
# tokenization to detect these patterns only after keywords aren't
# first found.
spec = {
    "assign": new_token(Tk.ASSIGN, ":="),
    "left_paren": new_token(Tk.LEFT_PAREN, "("),
    "right_paren": new_token(Tk.RIGHT_PAREN, ")"),
    "dot": new_token(Tk.DOT, "."),
    "lambda": new_token(Tk.LAMBDA, "\\"),
    "def": new_token(Tk.DEF, "def"),
    "sym": new_token(Tk.SYM, "sym"),
    "space": new_token(Tk.SPACE, " ", r"[\t ]"),
    "name": new_token(Tk.NAME, "", IDENT),
    "error": new_token(Tk.ERROR, "", r"."),
}


def tokenize(raw_term: str) -> "list[Token] | err.LambdaError":
    pats = [f"(?P<{label}>{t["regex"]})" for (label, t) in spec.items()]
    token_pattern = "|".join(pats)

    tokens: list[Token] = []

    # Track the current iteration index, to make IllegalTokenError
    # consistent with other errors.
    i = 0
    for mobj in re.finditer(token_pattern, raw_term):
        label = mobj.lastgroup

        if label is None:
            raise ValueError("Fatal: found 'None'")

        value = mobj.group()

        match label:
            case "name":
                tokens.append(name_t(value))
            case "error":
                return err.error(tokens, i, err.Err.ILLEGAL_TOKEN)
            case "space":
                continue
            case _:
                tokens.append(spec[label])

        i += 1

    return tokens
