import lbd.term as term


def shift(ast: term.AST, amount: int, minimum: int) -> None:
    """Shift names of at least MINIMUM value inside AST by AMOUNT.

    This doesn't actually get used; rather it's used to implement INC
    and DEC, which see.

    """

    match ast:
        case term.Name():
            if ast.index >= minimum:
                ast.index += amount
                ast.depth += amount

        case term.Abstraction():
            shift(ast.body, amount, minimum + 1)

        case term.Application():
            shift(ast.left, amount, minimum)
            shift(ast.right, amount, minimum)

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast}")


def inc(ast: term.AST, minimum: int):
    """Shift names of at least MINIMUM value inside AST up by 1."""

    shift(ast, 1, minimum)


def dec(ast: term.AST, minimum: int):
    """Shift names of at least MINIMUM value inside AST down by 1. """

    shift(ast, -1, minimum)


def replace(ast: term.AST, argument: term.AST, target_index: int):
    """Replace TARGET_INDEX inside AST with ARGUMENT, another AST.

    Return the modified AST."""

    match ast:
        case term.Name():
            if ast.index == target_index:
                return argument

            return ast

        case term.Abstraction():
            inc(argument, 0)
            new_body = replace(ast.body, argument, target_index + 1)

            return term.Abstraction(label=None, body=new_body)

        case term.Application():
            new_left = replace(ast.left, argument, target_index)
            new_right = replace(ast.right, argument, target_index)

            return term.Application(label=None, left=new_left, right=new_right)

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast}")


def beta_reduce(ast: term.AST) -> term.AST:
    """Evaluate AST using normal order beta reduction.

    Return the reduced AST.

    """

    match ast:
        case term.Name() | term.Abstraction():
            return ast

        case term.Application():
            beta_left = beta_reduce(ast.left)

            if not isinstance(beta_left, term.Abstraction):
                beta_right = beta_reduce(ast.right)

                return term.Application(label=None, left=beta_left, right=beta_right)

            fn = beta_left
            arg = ast.right

            # Actual beta redux algorithm.
            inc(arg, 0)
            replaced_body = replace(fn.body, arg, 0)
            dec(replaced_body, 0)

            return beta_reduce(replaced_body)

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast}")
