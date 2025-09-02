import re
from dataclasses import dataclass

import lbd.error as err
import lbd.token_defs as tdef

IDENT = r"[A-Za-z_]\w*"


@dataclass
class Token():
    kind: tdef.Tk
    name: str
    value: str
    regex: str

    def __str__(self):
        if self.kind == tdef.Tk.NAME:
            return f"name({self.value})"

        return f"{self.name}"


def new_token(kind: tdef.Tk, value: str, regex: str | None = None) -> Token:
    if regex is None:
        regex = re.escape(value)

    return Token(kind, kind.name.lower(), value, regex)


def name_t(value: str):
    return new_token(tdef.Tk.NAME, value, IDENT)


def error_t(value: str):
    return new_token(tdef.Tk.ERROR, value, r".")


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


def define_spec() -> dict[str, Token]:
    spec: dict[str, Token] = dict()

    for tk in tdef.Tk:
        enum_name = tk.name.lower()
        (_, enum_value) = tk.value

        if enum_value != "":
            spec[enum_name] = new_token(tk, enum_value)

    # Singleton cases. These must be added after spec is initialized with
    # the other, constant tokens. This is because the order in which
    # entries are added to spec affects the regex-based tokenization used.
    spec["space"] = new_token(tdef.Tk.SPACE, " ", r"[\t ]")
    spec["name"] = new_token(tdef.Tk.NAME, "", IDENT)
    spec["error"] = new_token(tdef.Tk.ERROR, "", r".")

    return spec


spec = define_spec()


def tokenize(raw_term: str) -> "list[Token] | err.LambdaError":
    pats = [f"(?P<{label}>{t.regex})" for (label, t) in spec.items()]
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
                tokens.append(name_t(value))
            case "error":
                tokens.append(error_t(value))

                if error_idx is None:
                    error_idx = i

            case "space":
                continue
            case "comment":
                break
            case _:
                tokens.append(spec[label])

        i += 1

    if error_idx is not None:
        return err.error(tokens, error_idx, err.Err.ILLEGAL_TOKEN)

    return tokens
