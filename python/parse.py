import enum
import itertools
import re

import error as err

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"

global_env = []


class Term(enum.StrEnum):
    NAME = "name"
    ABSTRACTION = "abstraction"
    APPLICATION = "application"

    def __repr__(self):
        return self


def new_name(index):
    """Construct and return a name with the given INDEX."""

    return {
        "kind": Term.NAME,
        "index": index,
    }


def new_abstraction(body):
    """Construct and return an abstraction with the given BODY."""

    return {
        "kind": Term.ABSTRACTION,
        "body": body,
    }


def new_application(left, right):
    """Construct and return an application with the given LEFT and
    RIGHT terms."""

    return {
        "kind": Term.APPLICATION,
        "left": left,
        "right": right,
    }

# What follows is a series of parse functions for a recursive-descent
# apparatus. As a rule, they accept the tokenized expression (given as
# a list of tokens), along with an index value pointing to the first
# token comprising the expression to be parsed, and finally the
# current environment merely consisting of the list of
# parameter-binders seen so far "above" us.
#
# The functions return the product of the parsing - the AST - along
# with the index of the first token that lies past the expression just
# parsed.


def parse_application(tokens, i, env):
    """Return a parsed application, as well as the index corresponding
    to the start of the next lambda term."""

    # Skip the left parenthesis.
    i += 1

    # Bootstrap the left-fold.
    first_term, i = parse_term(tokens, i, env[:])
    second_term, i = parse_term(tokens, i, env[:])
    partial = new_application(first_term, second_term)

    while tokens[i] != ")":
        next_term, i = parse_term(tokens, i, env[:])
        partial = new_application(partial, next_term)

    # Skip the closing parenthesis.
    i += 1

    return partial, i


def parse_abstraction(tokens, i, env):
    # Skip the lambda symbol.
    i += 1

    # Record the formal parameter inside env.
    env.append(tokens[i])

    if tokens[i + 1] != ".":
        raise err.AbstractionNoDotError(i + 1, tokens)

    # Move past the dot.
    i += 2

    body, i = parse_term(tokens, i, env[:])

    return new_abstraction(body), i


def parse_name(tokens, i, env):
    for (name, ast) in reversed(global_env):
        if name == tokens[i]:
            return ast, i + 1

    try:
        name = new_name(list(reversed(env)).index(tokens[i]))
        i += 1

        return name, i
    except ValueError:
        raise err.UnboundNameError(i, tokens[i])


def parse_term(tokens, i, env):
    """Parse TOKENS and return a parse tree (along with the current
    index into TOKENS.)"""

    if tokens[i] == "(":
        return parse_application(tokens, i, env[:])
    elif tokens[i] == "\\":
        return parse_abstraction(tokens, i, env[:])
    elif re.fullmatch(IDENT, tokens[i]):
        return parse_name(tokens, i, env[:])
    else:
        raise err.StrayTokenError(i, tokens[i])


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


def parse(raw_term):
    """Given RAW_TERM, construct an AST.

    Return AST along with the number of tokens parsed.

    """

    tokens = tokenize(raw_term)
    err.ParseError.set_tokens(tokens)

    label = None

    # If applicable, record the name to be added to the global
    # environment.
    if tokens[0] == "def":
        # Note that we do this before we alter tokens so that the
        # parser sees our augmented result.
        label = tokens[1]

        # Move the left-side params to the right side as lambda
        # binders.
        mid = tokens.index(":=")

        params = tokens[2:mid]
        body = tokens[mid+1:]
        fn_prefix = list(itertools.chain.from_iterable(
            [["\\", f"{p}", "."] for p in params]))

        tokens = fn_prefix + body

    # Parse the now preprocessed term.
    try:
        ast, num_tokens_parsed = parse_term(tokens, 0, [])

        if num_tokens_parsed < len(tokens):
            raise err.TrailingGarbageError(num_tokens_parsed, tokens)

        if label is not None:
            global_env.append((label, ast))

        return ast, num_tokens_parsed
    except IndexError:
        raise err.IncompleteTermError(len(tokens), tokens)
