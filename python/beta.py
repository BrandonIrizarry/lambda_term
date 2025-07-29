from parse import Term
from parse import new_name as N
from parse import new_abstraction as F
from parse import new_application as A


def shift(ast, amount, minimum):
    """Shift names of at least MINIMUM value inside AST by AMOUNT."""

    if ast["kind"] == Term.NAME:
        if ast["index"] >= minimum:
            ast["index"] += 1
    elif ast["kind"] == Term.ABSTRACTION:
        shift(ast["body"], amount, minimum + 1)
    elif ast["kind"] == Term.APPLICATION:
        shift(ast["left"], amount, minimum)
        shift(ast["right"], amount, minumum)
    else:
        raise ValueError

if __name__ == "__main__":
    ast1 = N(0)

    shift(ast1, 1, 0)

    print(ast1)

    ast2 = F(N(1))

    shift(ast2, 1, 0)

    print(ast2)
