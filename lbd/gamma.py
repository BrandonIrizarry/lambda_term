from dataclasses import dataclass

from lbd.term import AST


@dataclass
class Symbol():
    """Associate a symbol name with its definition."""
    label: str
    ast: AST | None


_gamma: list[Symbol] = []


def gamma(target: str) -> int | None:
    """Return the index of FREE_NAME inside gamma.

    If not found, return None.

    """

    for i, sym in enumerate(_gamma):
        label = sym.label

        if label == target:
            return i

    return None


def sym_get(index: int) -> Symbol | None:
    try:
        return _gamma[index]
    except ValueError:
        return None


def sym_declare(free_name: str) -> int:
    """Add FREE_NAME to gamma."""

    idx = gamma(free_name)

    # If the symbol has already been declared, do nothing; simply
    # return the index where the symbol was found.
    if idx is not None:
        return idx

    new_symbol = Symbol(label=free_name, ast=None)
    _gamma.append(new_symbol)

    return len(_gamma) - 1


def sym_set(sym_name: str, ast: AST | None) -> bool:
    """Set the definition of SYM_NAME to AST.

    An AST of 'None' instructs to clear the definition.

    Return whether the symbol was found.

    """

    idx = gamma(sym_name)

    if idx is None:
        return False

    _gamma[idx].ast = ast

    return True


def sym_find(sym_name: str) -> tuple[AST | None, bool]:
    """Find the AST value associated with SYM_NAME.

    In addition to the AST, return a flag signifying whether the
    variable is missing, or else present but simply unassigned
    (corresponding to False and True, respectively.)

    """

    idx = gamma(sym_name)

    if idx is None:
        return None, False

    return _gamma[idx].ast, True


def sym_clear(sym_name: str) -> bool:
    """Clear the AST-defintion of SYM_NAME.

    Return whether the symbol was found.

    """

    return sym_set(sym_name, None)


def sym_delete(sym_name: str) -> bool:
    """Remove SYM_NAME's status as a free symbol.

    Return whether the symbol was found.

    """

    idx = gamma(sym_name)

    if idx is None:
        return False

    del _gamma[idx]

    return True
