from typing import Any

import lbd.term as term


def shift(ast, amount, minimum):
    """Shift names of at least MINIMUM value inside AST by AMOUNT.

    This doesn't actually get used; rather it's used to implement INC
    and DEC, which see.

    """

    match ast["kind"]:
        case term.Term.NAME:
            if ast["index"] >= minimum:
                ast["index"] += amount

        case term.Term.ABSTRACTION:
            shift(ast["body"], amount, minimum + 1)

        case term.Term.APPLICATION:
            shift(ast["left"], amount, minimum)
            shift(ast["right"], amount, minimum)

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast["kind"]}")


def inc(ast, minimum):
    """Shift names of at least MINIMUM value inside AST up by 1."""

    shift(ast, 1, minimum)


def dec(ast, minimum):
    """Shift names of at least MINIMUM value inside AST down by 1. """

    shift(ast, -1, minimum)


def replace(ast, argument, target_index):
    """Replace TARGET_INDEX inside AST with ARGUMENT, another AST.

    Return the modified AST."""

    match ast["kind"]:
        case term.Term.NAME:
            if ast["index"] == target_index:
                return argument

            return ast

        case term.Term.ABSTRACTION:
            inc(argument, 0)
            new_body = replace(ast["body"], argument, target_index + 1)

            return term.new_abstraction(new_body)

        case term.Term.APPLICATION:
            new_left = replace(ast["left"], argument, target_index)
            new_right = replace(ast["right"], argument, target_index)

            return term.new_application(new_left, new_right)

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast["kind"]}")


def beta_reduce(ast) -> dict[str, Any]:
    """Evaluate AST using normal order beta reduction.

    Return the reduced AST.

    """

    match ast["kind"]:
        case term.Term.NAME | term.Term.ABSTRACTION:
            return ast

        case term.Term.APPLICATION:
            beta_left = beta_reduce(ast["left"])

            if beta_left["kind"] != term.Term.ABSTRACTION:
                beta_right = beta_reduce(ast["right"])

                return term.new_application(beta_left, beta_right)

            fn = beta_left
            arg = ast["right"]

            # Actual beta redux algorithm.
            inc(arg, 0)
            replaced_body = replace(fn["body"], arg, 0)
            dec(replaced_body, 0)

            return beta_reduce(replaced_body)

        case _:
            raise ValueError(f"Fatal: invalid ast-kind: {ast["kind"]}")
