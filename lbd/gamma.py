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


def sym_declare(free_name: str) -> None:
    """Add FREE_NAME to gamma."""

    new_symbol: Symbol = {"name": free_name, "ast": None}
    _gamma.append(new_symbol)


def sym_set(sym_name: str, ast: AST | None, delete: bool = False) -> bool:
    """Set the definition of SYM_NAME to AST.

    An AST of 'None' instructs to clear the definition; the DELETE
    flag instructs to remove the free symbol entirely from _gamma.

    Return whether the symbol was found.

    """

    found = False

    for i in range(len(_gamma)):
        if _gamma[i]["name"] == sym_name:
            if delete:
                del _gamma[i]
            else:
                _gamma[i]["ast"] = ast

            found = True

    return found


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


def debruijn(free_name: str, offset: int) -> int | None:
    """Compute the effective DeBruijn index of FREE_NAME.

    OFFSET is meant to be the length of the current local environment
    kept track of by the parser.

    """

    index = gamma(free_name)

    if index is None:
        return index

    return offset + index
