import lbd.error as err
import lbd.gamma as gamma
import lbd.term as term
import lbd.tokenize_lambda as tkz

# What follows is a series of parse functions for a recursive-descent
# apparatus. As a rule, they accept the tokenized expression (given as
# a list of tokens), along with an index value pointing to the first
# token comprising the expression to be parsed, and finally the
# current environment merely consisting of the list of
# parameter-binders seen so far "above" us.
#
# The functions normally return the product of the parsing - the AST -
# along with the index of the first token that lies past the
# expression just parsed. If an Exception is found, return that
# instead.


def parse_application(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.AST, int] | Exception:
    """Return a parsed application, as well as the index corresponding
    to the start of the next lambda term."""

    # Skip the left parenthesis.
    i += 1

    # Bootstrap the left-fold.
    _first = parse_term(tokens, i, env[:])

    if isinstance(_first, Exception):
        return _first

    first_term, i = _first

    _second = parse_term(tokens, i, env[:])

    if isinstance(_second, Exception):
        return _second

    second_term, i = _second

    # What follows is our implementation of sugar for writing
    # applications, given that these are left-associative. For
    # example, (a b c d e) becomes ((((a b) c) d) e). Otherwise, here
    # we would simply stop here, skipping the right paren and
    # returning the newly created application-term.
    #
    # Here I use an iterative version of fold-left, where 'partial' is
    # the accumulator variable.

    # Start with (a b).
    partial = term.new_application(first_term, second_term)

    while True:
        # Get the next token in the application-expression list, or
        # possibly the terminating right-parenthesis.
        t = tkz.get(tokens, i)

        if t is None:
            return err.parsing(tokens, i, err.Err.INCOMPLETE)

        if tkz.is_right_paren_t(t):
            break

        # The next token signifies the beginning of the next _term_ in
        # the list, so parse that.
        _next = parse_term(tokens, i, env[:])

        if isinstance(_next, Exception):
            return _next

        # Here we update i to advance the loop.
        next_term, i = _next

        # The accumulation step.
        partial = term.new_application(partial, next_term)

    # Skip the closing parenthesis.
    i += 1

    return partial, i


def parse_abstraction(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.AST, int] | Exception:
    # Skip the lambda symbol.
    i += 1

    # Record the formal parameter inside env.
    param = tkz.get(tokens, i)

    if param is None:
        return err.parsing(tokens, i, err.Err.MISSING_PARAM)

    if not tkz.is_name_t(param):
        return err.parsing(tokens, i, err.Err.INVALID_PARAM)

    env.append(param["str"])

    # Advance; we should then be on the dot.
    i += 1

    dot = tkz.get(tokens, i)

    if dot is None:
        return err.parsing(tokens, i, err.Err.INCOMPLETE)

    if not tkz.is_dot_t(dot):
        return err.parsing(tokens, i, err.Err.MISSING_DOT)

    # Advance; we should then be at the start of the body.
    i += 1

    _body = parse_term(tokens, i, env[:])

    if isinstance(_body, Exception):
        return _body

    body, i = _body

    return term.new_abstraction(body), i


def parse_name(tokens: list[tkz.Token], i: int, env: list[str]):
    # Search for the current name across the local env, starting from
    # the back (using a LIFO discipline, since we're implementing
    # layered function scopes.)
    is_local = False
    index = 0

    t = tkz.get(tokens, i)

    if t is None:
        return err.parsing(tokens, i, err.Err.INCOMPLETE)

    name = t["str"]

    for local_name in reversed(env):
        # FIXME: we expect this key to exist, so we should probably
        # change the function signature.
        if local_name == name:
            is_local = True
            break

        index += 1

    if is_local:
        return term.new_name(index), i + 1

    free_index = gamma.debruijn(name, len(env))

    return term.new_name(free_index), i + 1


def parse_term(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.AST, int] | Exception:
    """Parse TOKENS and return a parse tree (along with the current
    index into TOKENS.)"""

    if len(tokens[i:]) == 0:
        return err.parsing(tokens, i, err.Err.INCOMPLETE)

    if tkz.is_left_paren_t(tokens[i]):
        return parse_application(tokens, i, env[:])
    elif tkz.is_lambda_t(tokens[i]):
        return parse_abstraction(tokens, i, env[:])
    elif tkz.is_name_t(tokens[i]):
        return parse_name(tokens, i, env[:])
    else:
        return err.parsing(tokens, i, err.Err.MEANINGLESS)
