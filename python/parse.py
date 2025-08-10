import enum

import desugar as dsg
import error as err
import tokenize_lambda as tkz


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


def parse_application(tokens, i, env, genv):
    """Return a parsed application, as well as the index corresponding
    to the start of the next lambda term."""

    # Skip the left parenthesis.
    i += 1

    # Bootstrap the left-fold.
    first_term, i = parse_term(tokens, i, env[:], genv)
    second_term, i = parse_term(tokens, i, env[:], genv)
    partial = new_application(first_term, second_term)

    while not tkz.is_right_paren_t(tokens[i]):
        next_term, i = parse_term(tokens, i, env[:], genv)
        partial = new_application(partial, next_term)

    # Skip the closing parenthesis.
    i += 1

    return partial, i


def parse_abstraction(tokens, i, env, genv):
    # Skip the lambda symbol.
    i += 1

    # Record the formal parameter inside env.
    if not tkz.is_name_t(tokens[i]):
        raise err.IllegalTokenError(i, tokens[i])

    env.append(tokens[i]["value"])

    if not tkz.is_dot_t(tokens[i + 1]):
        raise err.AbstractionNoDotError(i + 1, tokens)

    # Move past the dot.
    i += 2

    body, i = parse_term(tokens, i, env[:], genv)

    return new_abstraction(body), i


def parse_name(tokens, i, env, genv):
    # Search for the current name across the local env, starting from
    # the back (using a LIFO discipline, since we're implementing
    # layered function scopes.)
    is_local = False
    index = 0

    for local_name in reversed(env):
        # FIXME: we expect this key to exist, so we should probably
        # change the function signature.
        if local_name == tokens[i]["value"]:
            is_local = True
            break

        index += 1

    if is_local:
        return new_name(index), i + 1

    # Else, check the global environment.
    for gdef in reversed(genv):
        if gdef["label"] == tokens[i]["value"]:
            return gdef["ast"], i + 1

    raise err.UnboundNameError(i, tokens[i])


def parse_term(tokens, i, env, genv):
    """Parse TOKENS and return a parse tree (along with the current
    index into TOKENS.)"""

    if tkz.is_left_paren_t(tokens[i]):
        return parse_application(tokens, i, env[:], genv)
    elif tkz.is_lambda_t(tokens[i]):
        return parse_abstraction(tokens, i, env[:], genv)
    elif tkz.is_name_t(tokens[i]):
        return parse_name(tokens, i, env[:], genv)
    else:
        raise err.StrayTokenError(i, tokens[i])


def parse(raw_term, genv):
    """Given RAW_TERM, construct an AST.

    Return AST along with the number of tokens parsed.

    """

    tokens = tkz.tokenize(raw_term)
    err.ParseError.set_tokens(tokens)

    tokens, label = dsg.desugar_def(tokens[:])

    # Parse the now preprocessed term.
    try:
        ast, num_tokens_parsed = parse_term(tokens, 0, [], genv)

        if num_tokens_parsed < len(tokens):
            raise err.TrailingGarbageError(num_tokens_parsed, tokens)

        return ast, num_tokens_parsed, label
    except IndexError:
        raise err.IncompleteTermError(len(tokens), tokens)
