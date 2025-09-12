import re
from dataclasses import dataclass

import lbd.error as err
import lbd.token_defs as tdef


@dataclass
class Token():
    kind: tdef.Tk
    value: str | None = None

    def __post_init__(self):
        if self.value is None:
            self.value = self.kind.value.label

    def __str__(self):
        if self.kind == tdef.Tk.NAME:
            return f"name({self.value})"

        return f"{self.kind.name}"


def get(tokens: list[Token], pos: int) -> Token | None:
    """Return the token at position POS.

    If POS is out of range, then return None.

    """

    if pos < 0:
        raise ValueError(f"Fatal: negative token-buffer index {pos}")

    if pos >= len(tokens):
        return None

    return tokens[pos]


def find(tokens: list[Token], token: Token) -> int | None:
    """Return the first index where TOKEN is found in TOKENS.

    If not found, return None.

    """

    for i in range(len(tokens)):
        if tokens[i] == token:
            return i

    return None


def tokenize(raw_term: str) -> "list[Token] | err.LambdaError":
    pats = []

    for tk in tdef.Tk:
        subpat = f"(?P<{tk.name.lower()}>{tk.value.regex})"
        pats.append(subpat)

    token_pattern = "|".join(pats)

    tokens: list[Token] = []

    # Track the current iteration index, to flag the position of any
    # ILLEGAL_TOKEN error.
    #
    # Flag the position of the first illegal token so that the
    # returned error can use the entire 'tokens' buffer (as opposed to
    # immediately returning, which necessarily truncates this
    # information.)
    i = 0
    error_idx = None

    for mobj in re.finditer(token_pattern, raw_term):
        label = mobj.lastgroup

        if label is None:
            raise ValueError("Fatal: found 'None'")

        value = mobj.group()

        match label:
            case "name":
                new_name = Token(tdef.Tk.NAME, value)
                tokens.append(new_name)
            case "error":
                new_error = Token(tdef.Tk.ERROR, value)
                tokens.append(new_error)

                if error_idx is None:
                    error_idx = i

            case "space":
                continue
            case _:
                tk = tdef.Tk[f"{label.upper()}"]
                tokens.append(Token(tk))

        i += 1

    if error_idx is not None:
        return err.error(tokens, error_idx, err.Err.ILLEGAL_TOKEN)

    return tokens
