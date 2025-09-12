import lbd.error as err
import lbd.gamma as gamma
import lbd.term as term
import lbd.token_defs as tdef
import lbd.tokenize as tkz

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


def parse_application(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.Application, int] | err.LambdaError:
    """Parse an application.

    Applications are of the form: (TERM TERM)

    Return a parsed application, as well as the index corresponding
    to the start of the next lambda term.

    """

    # Skip the left parenthesis.
    i += 1

    # Bootstrap the left-fold.
    _first = parse_term(tokens, i, env)

    if isinstance(_first, err.LambdaError):
        return _first

    first_term, i = _first

    _second = parse_term(tokens, i, env)

    if isinstance(_second, err.LambdaError):
        return _second

    second_term, i = _second

    # What follows is our implementation of sugar for writing
    # applications, given that these are left-associative. For
    # example, (a b c d e) becomes ((((a b) c) d) e).
    #
    # Here I use an iterative version of fold-left, where 'partial' is
    # the accumulator variable.

    # Start with (a b).
    partial = term.Application(first_term, second_term)

    while True:
        # Get the next token in the application-expression list, or
        # possibly the terminating right-parenthesis.
        t = tkz.get(tokens, i)

        if t is None:
            return err.error(tokens, i, err.Err.INCOMPLETE)

        if t == tkz.Token(tdef.Tk.RIGHT_PAREN):
            break

        # The next token signifies the beginning of the next _term_ in
        # the list, so parse that.
        _next = parse_term(tokens, i, env)

        if isinstance(_next, err.LambdaError):
            return _next

        # Here we update i to advance the loop.
        next_term, i = _next

        # The accumulation step.
        partial = term.Application(partial, next_term)

    # Skip the closing parenthesis.
    i += 1

    return partial, i


def parse_abstraction(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.Abstraction, int] | err.LambdaError:
    """Parse an abstraction.

    Abstractions are of the form: \\NAME.TERM

    Return the parsed abstraction.

    """

    # Skip the lambda symbol.
    i += 1

    # Record the formal parameter inside env.
    param = tkz.get(tokens, i)

    if param is None:
        return err.error(tokens, i, err.Err.MISSING_PARAM)

    if param.kind != tdef.Tk.NAME:
        return err.error(tokens, i, err.Err.INVALID_PARAM)

    if param.value is None:
        raise ValueError(f"Fatal: '{param}' value field was never set")

    subenv = [param.value]

    # Advance; we should then be on the dot.
    i += 1

    dot = tkz.get(tokens, i)

    if dot is None:
        return err.error(tokens, i, err.Err.INCOMPLETE)

    if dot != tkz.Token(tdef.Tk.DOT):
        return err.error(tokens, i, err.Err.MISSING_DOT)

    # Advance; we should then be at the start of the body.
    i += 1

    _body = parse_term(tokens, i, [*env, *subenv])

    if isinstance(_body, err.LambdaError):
        return _body

    body, i = _body

    return term.Abstraction(body), i


def parse_name(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.Name, int] | err.LambdaError:
    """Parse a name.

    A name is valid (for now) if and only if it could be a valid C
    identifier.

    This function identifies the given name-token's (already
    predetermined) place in the function-scope hierarchy: that is,
    it'll either be identified as a bound local name, or else a free
    name. Either way, a new Name term will be returned, with its
    DeBruijn index set according to that circumstance.

    Return the parsed name, or else a parse-error.

    """

    # Search for the current name across the local env, starting from
    # the back (using a LIFO discipline, since we're implementing
    # layered function scopes.)
    is_local = False
    index = 0

    name_t = tkz.get(tokens, i)

    if name_t is None:
        return err.error(tokens, i, err.Err.INCOMPLETE)

    if name_t.kind != tdef.Tk.NAME:
        return err.error(tokens, i, err.Err.INVALID_NAME)

    value = name_t.value

    if value is None:
        raise ValueError(f"Fatal: value field for '{name_t}' was never set")

    for local_name in reversed(env):
        if local_name == name_t.value:
            is_local = True
            break

        index += 1

    if is_local:
        return term.Name(index), i + 1

    # Treat the token as referring to a free name.
    free_index = gamma.gamma(value)

    if free_index is not None:
        return term.Name(free_index + len(env)), i + 1

    return err.error(tokens, i, err.Err.UNASSIGNED)


def parse_assignment(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.Assignment, int] | err.LambdaError:
    """Parse an assignment statement.

    Assignments are of the form <Name := Term>.

    Return the parsed Term.

    """

    # Skip 'def'.
    i += 1

    # Get the token corresponding to the assignee.
    name_t = tkz.get(tokens, i)

    if name_t is None:
        return err.error(tokens, i, err.Err.MISSING)

    if name_t.kind != tdef.Tk.NAME:
        return err.error(tokens, i, err.Err.INVALID_NAME)

    value = name_t.value

    if value is None:
        raise ValueError(f"Fatal: value field for '{name_t}' was never set")

    # Declare the new free name at parse time, since its DeBruijn
    # index, which depends on its gamma value, needs to be known
    # before beta reduction occurs.
    idx = gamma.sym_declare(value)
    name = term.Name(idx + len(env))

    # Skip the name manually, since we didn't (nor couldn't) use
    # 'parse_name' to obtain it.
    i += 1

    # Scan for any parameters given.
    params = []

    while (p := tkz.get(tokens, i)) != tkz.Token(tdef.Tk.ASSIGN):
        if p is None:
            return err.error(tokens, i, err.Err.INCOMPLETE)

        if p.kind != tdef.Tk.NAME:
            return err.error(tokens, i, err.Err.INVALID_PARAM)

        params.append(p)

        i += 1

    # Preemptively create a subenv. Note that, if params is empty,
    # subenv will be empty, and consequently [*env, *subenv] will
    # equal simply env, corresponding to the parameterless case, as
    # desired.
    subenv = [p.value for p in params]

    # Skip the assignment token.
    i += 1

    # This is where we parse the assigned value.

    # We should proceed with caution here, since, if subenv is
    # non-empty, it _must_ be wrapped accordingly with Abstractions,
    # else all the inner names will have the wrong depth values.
    _ast = parse_term(tokens, i, [*env, *subenv])

    if isinstance(_ast, err.LambdaError):
        return _ast

    ast, i = _ast

    # If params is non-empty, then by now, the environment of the
    # assigned value will have conveniently been extended.
    for p in params:
        ast = term.Abstraction(ast)

    return term.Assignment(name, ast), i


def parse_let(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.AST, int] | err.LambdaError:
    """Parse let expressions.

    A let expression is of the form

    let Name := Term in Term

    Note that 'let' and 'in' are keywords.

    This is basically returned as an application of the form

    (\\name.body value)

    The idea is to use logic similar to that used by
    'parse_abstraction' to construct the left hand side, and then
    parse the value so that we can return the final application term.

    """

    # Skip 'let'.
    i += 1

    # Record the let-name as a parameter inside env, as we would in
    # the case of an abstraction.
    param = tkz.get(tokens, i)

    if param is None:
        return err.error(tokens, i, err.Err.MISSING_PARAM)

    if param.kind != tdef.Tk.NAME:
        return err.error(tokens, i, err.Err.INVALID_PARAM)

    if param.value is None:
        raise ValueError(f"Fatal: value field for '{param}' was never set")

    subenv = [param.value]

    # Advance; check if we're on an assignment token.
    i += 1

    assign = tkz.get(tokens, i)

    if assign is None:
        return err.error(tokens, i, err.Err.INCOMPLETE)

    if assign != tkz.Token(tdef.Tk.ASSIGN):
        return err.error(tokens, i, err.Err.MISSING_ASSIGN_OP)

    # Advance to land on the let-value, and parse it using the
    # original env.
    i += 1

    _value = parse_term(tokens, i, env)

    if isinstance(_value, err.LambdaError):
        return _value

    value, i = _value

    # Now we should be on 'in'.
    in_t = tkz.get(tokens, i)

    if in_t is None:
        return err.error(tokens, i, err.Err.INCOMPLETE)

    if in_t != tkz.Token(tdef.Tk.IN):
        return err.error(tokens, i, err.Err.MISSING_IN_OP)

    # Skip the 'in', to move on to the body.
    i += 1

    # Note that here we finally use the subenv defined previously.
    _body = parse_term(tokens, i, [*env, *subenv])

    if isinstance(_body, err.LambdaError):
        return _body

    body, i = _body

    return term.Application(term.Abstraction(body), value), i


def parse_term(tokens: list[tkz.Token], i: int, env: list[str]) -> tuple[term.AST, int] | err.LambdaError:
    """Parse TOKENS, given index I and environment ENV.

    This function is used for parsing a general lambda term.

    Return a parse tree (along with the next position to parse inside
    TOKENS.)

    """

    if len(tokens[i:]) == 0:
        return err.error(tokens, i, err.Err.INCOMPLETE)

    match tokens[i].kind:
        case tdef.Tk.LEFT_PAREN:
            return parse_application(tokens, i, env)

        case tdef.Tk.LAMBDA:
            return parse_abstraction(tokens, i, env)

        case tdef.Tk.NAME:
            return parse_name(tokens, i, env)

        case tdef.Tk.DEF:
            return parse_assignment(tokens, i, env)

        case tdef.Tk.LET:
            return parse_let(tokens, i, env)

        case _:
            return err.error(tokens, i, err.Err.MEANINGLESS)
