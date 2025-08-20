import enum
import re

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


type Token = tuple[Tk, str]


ASSIGN = (Tk.ASSIGN, ":=")
LEFT_PAREN = (Tk.LEFT_PAREN, "(")
RIGHT_PAREN = (Tk.RIGHT_PAREN, ")")
DOT = (Tk.DOT, ".")
LAMBDA = (Tk.LAMBDA, "\\")
DEF = (Tk.DEF, "def")


def name_t(value: str):
    return (Tk.NAME, value)


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


def tokenize(raw_term: str) -> "list[Token] | err.LambdaError":
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
                tokens.append(ASSIGN)
            case "def":
                tokens.append(DEF)
            case "name":
                tokens.append(name_t(value))
            case "left_paren":
                tokens.append(LEFT_PAREN)
            case "right_paren":
                tokens.append(RIGHT_PAREN)
            case "dot":
                tokens.append(DOT)
            case "lambda":
                tokens.append(LAMBDA)
            case "space":
                continue
            case "error":
                return err.error(tokens, i, err.Err.ILLEGAL_TOKEN)

        i += 1

    return tokens
