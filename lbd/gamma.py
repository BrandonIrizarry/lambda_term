from dataclasses import dataclass, field

import lbd.term as term


@dataclass
class Symbol():
    """Associate a symbol name with its definition."""
    label: str
    ast: "term.AST" = field(default_factory=lambda: term.Empty())


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

    new_symbol = Symbol(free_name)
    _gamma.append(new_symbol)

    return len(_gamma) - 1


def sym_set(sym_name: str, ast: "term.AST") -> bool:
    """Set the definition of SYM_NAME to AST.

    Return whether the symbol was found.

    """

    idx = gamma(sym_name)

    if idx is None:
        return False

    _gamma[idx].ast = ast

    return True


def sym_find(sym_name: str) -> "term.AST | None":
    """Find the AST value associated with SYM_NAME."""

    idx = gamma(sym_name)

    if idx is None:
        return idx

    return _gamma[idx].ast


def sym_clear(index: int) -> None:
    """Clear the definition in _gamma at INDEX.

    This sets the definition to term.Empty().

    Such a symbol can be later reset to a different, non-empty AST.

    INDEX is expected to be a valid index into _gamma.

    """

    _gamma[index].ast = term.Empty()


def clear_gamma() -> None:
    """Reset gamma to an empty list."""

    _gamma.clear()
