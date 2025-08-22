from typing import TypedDict

from lbd.term import AST


class Symbol(TypedDict):
    """Associate a symbol name with its definition."""
    name: str
    ast: AST | None


_gamma: list[Symbol] = []


def gamma(free_name: str) -> int | None:
    """Return the index of FREE_NAME inside gamma.

    If not found, return None.

    """

    for i in range(len(_gamma)):
        n = _gamma[i]["name"]

        if n == free_name:
            return i

    return None


def sym_get(index: int) -> Symbol | None:
    try:
        return _gamma[index]
    except ValueError:
        return None


def sym_declare(free_name: str) -> int:
    """Add FREE_NAME to gamma."""

    new_symbol: Symbol = {"name": free_name, "ast": None}
    _gamma.append(new_symbol)

    return len(_gamma) - 1


def sym_set(sym_name: str, ast: AST | None, delete: bool = False) -> bool:
    """Set the definition of SYM_NAME to AST.

    An AST of 'None' instructs to clear the definition; the DELETE
    flag instructs to remove the free symbol entirely from _gamma.

    Return whether the symbol was found.

    """

    for i in range(len(_gamma)):
        if _gamma[i]["name"] == sym_name:
            if delete:
                del _gamma[i]
            else:
                _gamma[i]["ast"] = ast

            return True

    return False


def sym_find(sym_name: str) -> tuple[AST | None, bool]:
    """Find the AST value associated with SYM_NAME.

    In addition to the AST, return a flag signifying whether the
    variable is missing, or else present but simply unassigned
    (corresponding to False and True, respectively.)

    """

    for sym in _gamma:
        if sym["name"] == sym_name:
            return sym["ast"], True

    return None, False


def sym_clear(sym_name: str) -> bool:
    """Clear the AST-defintion of SYM_NAME.

    Return whether the symbol was found.

    """

    return sym_set(sym_name, None)


def sym_delete(sym_name: str) -> bool:
    """Remove SYM_NAME's status as a free symbol.

    Return whether the symbol was found.

    """

    return sym_set(sym_name, None, True)
