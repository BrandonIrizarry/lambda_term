import enum
import re


IDENT = r"[A-Za-z_][A-Za-z0-9_]*"


class Term(enum.StrEnum):
    NAME = "name"
    ABSTRACTION = "abstraction"
    APPLICATION = "application"

    def __repr__(self):
        return self


class IncompleteTermError(Exception):
    pass


class TrailingGarbageError(Exception):
    pass


class UnboundNameError(Exception):
    def __init__(self, position, name):
        self.position = position
        self.name = name

    def __str__(self):
        return "Name '{}' at token-position {} is unbound"\
            .format(self.name, self.position)


class StrayTokenError(Exception):
    def __init__(self, position, token):
        self.position = position
        self.token = token

    def __str__(self):
        return "Stray token '{}' at token-position {}"\
            .format(self.token, self.position)


class AbstractionNoDotError(Exception):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return "Missing dot-separator at token-position {}"\
            .format(self.position)


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


def parse_application(tokens, i, env):
    """Return a parsed application, as well as the index corresponding
    to the start of the next lambda term."""

    # Skip the left parenthesis.
    i += 1

    left, i = parse_term(tokens, i, env[:])
    right, i = parse_term(tokens, i, env[:])

    # Skip the closing parenthesis.
    i += 1

    return new_application(left, right), i


def parse_abstraction(tokens, i, env):
    # Skip the lambda symbol.
    i += 1

    # Record the formal parameter inside env.
    env.append(tokens[i])

    if tokens[i + 1] != ".":
        raise AbstractionNoDotError(i + 1)

    # Move past the dot.
    i += 2

    body, i = parse_term(tokens, i, env[:])

    return new_abstraction(body), i


def parse_name(tokens, i, env):
    try:
        name = new_name(len(env) - env.index(tokens[i]) - 1)
        i += 1

        return name, i
    except ValueError:
        raise UnboundNameError(i, tokens[i])


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
        raise StrayTokenError(i, tokens[i])


def tokenize(raw_term):
    token_pattern = r"[A-Za-z_][A-Za-z0-9_]*|[\\().]"
    return re.findall(token_pattern, raw_term)


def parse(raw_term):
    """Given RAW_TERM, construct an AST.

    Return AST along with the number of tokens parsed.

    """

    tokens = tokenize(raw_term)

    try:
        ast, num_tokens_parsed = parse_term(tokens, 0, [])

        if num_tokens_parsed < len(tokens):
            raise TrailingGarbageError

        return ast, num_tokens_parsed
    except IndexError:
        raise IncompleteTermError
