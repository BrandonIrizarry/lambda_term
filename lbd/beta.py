import lbd.gamma as g
import lbd.term as term


def _shift(ast: term.AST, amount: int, minimum: int) -> term.AST:
    """Shift names of at least MINIMUM value inside AST by AMOUNT.

    This function is used to implement INC and DEC. Otherwise, it
    should appear nowhere else.

    """

    match ast:
        case term.Name():
            if ast.index >= minimum:
                return term.Name(ast.index + amount)

            return ast

        case term.Abstraction():
            new_body = _shift(ast.body, amount, minimum + 1)

            return term.Abstraction(new_body)

        case term.Application():
            new_left = _shift(ast.left, amount, minimum)
            new_right = _shift(ast.right, amount, minimum)

            return term.Application(new_left, new_right)

        case term.Assignment():
            new_name = _shift(ast.name, amount, minimum)
            new_value = _shift(ast.value, amount, minimum)

            assert isinstance(new_name, term.Name)

            return term.Assignment(new_name, new_value)

        case term.Empty():
            return ast

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast}")


def inc(ast: term.AST, minimum: int) -> term.AST:
    """Shift names of at least MINIMUM value inside AST up by 1."""

    return _shift(ast, 1, minimum)


def dec(ast: term.AST, minimum: int) -> term.AST:
    """Shift names of at least MINIMUM value inside AST down by 1. """

    return _shift(ast, -1, minimum)


def replace(ast: term.AST, argument: term.AST, target_index: int) -> term.AST:
    """Replace TARGET_INDEX inside AST with ARGUMENT, another AST.

    Return the modified AST."""

    match ast:
        case term.Name():
            if ast.index == target_index:
                return argument

            return ast

        case term.Abstraction():
            new_argument = inc(argument, 0)
            new_body = replace(ast.body, new_argument, target_index + 1)

            return term.Abstraction(new_body)

        case term.Application():
            new_left = replace(ast.left, argument, target_index)
            new_right = replace(ast.right, argument, target_index)

            return term.Application(new_left, new_right)

        case term.Assignment():
            new_name = replace(ast.name, argument, target_index)
            new_value = replace(ast.value, argument, target_index)

            assert isinstance(new_name, term.Name)

            return term.Assignment(new_name, new_value)

        case term.Empty():
            return ast

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast}")


def beta_reduce(ast: term.AST) -> term.AST:
    """Evaluate AST using normal order beta reduction.

    Return the reduced AST.

    """

    match ast:
        # Some remarks on the Name() case:
        #
        # 1. The only time a name is evaluated is when it's a free
        # name, since otherwise we'd still be at the stage of
        # evaluating the abstraction binding that name.
        #
        # 2. Since the name isn't underneath any abstractions at this
        # point, its scope-depth is zero, and so its index as a Name
        # is precisely its index into gamma.
        case term.Name():
            if (idx := ast.index) < 0:
                raise ValueError(
                    f"Fatal: name with negative index of {ast.index}")

            sym = g.sym_get(idx)

            # For now, panic with a ValueError here.
            if sym is None:
                raise ValueError(f"Undefined free symbol (freeness {idx})")

            # Currently, 'sym.ast' can't assume a value of None, but
            # this could change in the future, hence I'm leaving this
            # check in place.
            elif sym.ast is None:
                raise ValueError(f"Unassigned free symbol '{sym.label}'")

            return beta_reduce(sym.ast)

        case term.Abstraction():
            return ast

        case term.Application():
            beta_left = beta_reduce(ast.left)

            match beta_left:
                case term.Abstraction():
                    fn = beta_left
                    arg = ast.right

                    # Actual beta redux algorithm.
                    new_arg = inc(arg, 0)
                    replaced_body = replace(fn.body, new_arg, 0)
                    new_replaced_body = dec(replaced_body, 0)

                    return beta_reduce(new_replaced_body)

                case _:
                    beta_right = beta_reduce(ast.right)

                    return term.Application(beta_left, beta_right)

        case term.Assignment():
            # The idea is to simply assign the AST to the given name,
            # which will be evaluated later as need be, under the
            # term.Name() case.
            if (idx := ast.name.index) < 0:
                f"Fatal: name with negative index of {idx}"

            sym = g.sym_get(idx)

            if sym is None:
                raise ValueError(f"Fatal: '{ast.name}' isn't a free symbol")

            beta_value = ast.value

            g.sym_set(sym.label, beta_value)

            return beta_value

        case term.Empty():
            return ast

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast}")
