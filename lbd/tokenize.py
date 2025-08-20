import enum
import re

import lbd.error as err
from typing import TypedDict

IDENT = r"[A-Za-z_]\w*"


class Tk(enum.StrEnum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    ASSIGN = ":="
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    DOT = "."
    LAMBDA = "\\"
    DEF = "def"
    SYM = "sym"
    SPACE = ""
    NAME = ""
    ERROR = ""


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


spec = dict()

for tk in Tk:
    enum_name = tk.name.lower()
    enum_value = tk.value

    if enum_value != "":
        spec[enum_name] = new_token(tk, enum_value)

# Singleton cases. These must be added after spec is initialized with
# the other, constant tokens. This is because the order in which
# entries are added to spec affects the regex-based tokenization used.
spec["space"] = new_token(Tk.SPACE, " ", r"[\t ]")
spec["name"] = new_token(Tk.NAME, "", IDENT)
spec["error"] = new_token(Tk.ERROR, "", r".")


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
