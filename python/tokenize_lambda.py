import re

import error as err

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"


def tokenize(raw_term):
    spec = [
        ("assign", ":="),
        ("name", IDENT),
        ("other", r"[\\().]"),
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
        value = mobj.group()

        if kind == "error":
            raise err.IllegalTokenError(i, value)

        if kind != "space":
            tokens.append(value)

        i += 1

    return tokens
