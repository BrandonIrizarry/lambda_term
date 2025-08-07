import re

import error as err

IDENT = r"[A-Za-z_]\w*"


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

        if kind == "error":
            raise err.IllegalTokenError(i, value)

        if kind == "space":
            continue

        tokens.append(value)

        i += 1

    return tokens
