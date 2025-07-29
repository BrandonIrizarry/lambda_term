from parse import Term
from parse import new_name
from parse import new_abstraction
from parse import new_application

N = new_name
F = new_abstraction
A = new_application


def shift(ast, amount, minimum):
    """Shift names of at least MINIMUM value inside AST by AMOUNT.

    This doesn't actually get used; rather it's used to implement INC
    and DEC, which see.

    """

    if ast["kind"] == Term.NAME:
        if ast["index"] >= minimum:
            ast["index"] += 1
    elif ast["kind"] == Term.ABSTRACTION:
        shift(ast["body"], amount, minimum + 1)
    elif ast["kind"] == Term.APPLICATION:
        shift(ast["left"], amount, minimum)
        shift(ast["right"], amount, minimum)
    else:
        raise ValueError


def inc(ast, minimum):
    """Shift names of at least MINIMUM value inside AST up by 1."""

    shift(ast, 1, minimum)


def dec(ast, minimum):
    """Shift names of at least MINIMUM value inside AST down by 1. """

    shift(ast, -1, minimum)


def replace(ast, argument, target_index):
    """Replace TARGET_INDEX inside AST with ARGUMENT, another AST.

    Return the modified AST."""
    if ast["kind"] == Term.NAME:
        if ast["index"] == target_index:
            return argument

        return ast
    elif ast["kind"] == Term.ABSTRACTION:
        inc(argument, 0)
        new_body = replace(ast["body"], argument, target_index + 1)

        return new_abstraction(new_body)
    elif ast["kind"] == Term.APPLICATION:
        new_left = replace(ast["left"], argument, target_index)
        new_right = replace(ast["right"], argument, target_index)

        return new_application(new_left, new_right)
    else:
        raise ValueError


def beta_reduce(ast):
    """Evaluate AST using normal order beta reduction.

    Return the reduced AST.

    """

    if ast["kind"] != Term.APPLICATION:
        return ast

    beta_left = beta_reduce(ast["left"])

    if beta_left["kind"] != Term.ABSTRACTION:
        beta_right = beta_reduce(ast["right"])

        return new_application(beta_left, beta_right)

    fn = beta_left
    arg = ast["right"]

    # Actual beta redux algorithm.
    inc(arg, 0)
    replaced_body = replace(fn["body"], arg, 0)
    dec(replaced_body, 0)

    return beta_reduce(replaced_body)


if __name__ == "__main__":
    identity = F(N(0))
    self_apply = F(A(N(0), N(0)))

    ast = A(identity, self_apply)

    new_ast = beta_reduce(ast)

    print(new_ast)
