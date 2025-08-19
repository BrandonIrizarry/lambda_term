import enum
import re
import typing

import lbd.error as err

IDENT = r"[A-Za-z_]\w*"


class Tk(enum.StrEnum):
    ASSIGN = ":="
    NAME = ""
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    DOT = "."
    LAMBDA = "\\"
    DEF = "."


class Token(typing.NamedTuple):
    kind: Tk
    value: str | None = None

    def __str__(self):
        if self.value is None:
            assert self.kind is not Tk.NAME

            return self.kind.value

        return self.value


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
                tokens.append(Token(Tk.ASSIGN))
            case "def":
                tokens.append(Token(Tk.DEF))
            case "name":
                tokens.append(Token(Tk.NAME, value))
            case "left_paren":
                tokens.append(Token(Tk.LEFT_PAREN))
            case "right_paren":
                tokens.append(Token(Tk.RIGHT_PAREN))
            case "dot":
                tokens.append(Token(Tk.DOT))
            case "lambda":
                tokens.append(Token(Tk.LAMBDA))
            case "space":
                continue
            case "error":
                return err.error(tokens, i, err.Err.ILLEGAL_TOKEN)

        i += 1

    return tokens
