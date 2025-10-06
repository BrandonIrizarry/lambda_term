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


_counter = 0


def new_refname():
    global _counter

    name = f"__{_counter}"
    _counter += 1

    return name


def sym_clear_thunks(prefix: str) -> None:
    """Clear all Symbols that start with the given PREFIX.

    This is intended to be used to clear out thunked refs after
    unwrapping them, so that the next evaluation can start afresh at,
    say, __0.

    The idea is that such thunks are detectable because they're marked
    with a prefix such as '__', or else '$'.

    """
    global _counter

    # Don't forget to reset the counter!
    #
    # As of yet, we have two pieces of persistent state to watch
    # whenever a reduction is performed: _gamma, and _counter.
    _counter = 0

    for i, sym in enumerate(_gamma):
        if sym.label.startswith(prefix):
            sym_clear(i)


def sym_clear(index: int) -> None:
    """Clear the definition in _gamma at INDEX.

    This sets the definition to term.Empty().

    Such a symbol can be later reset to a different, non-empty AST.

    INDEX is expected to be a valid index into _gamma.

    """

    _gamma[index].ast = term.Empty()


def clear_gamma() -> None:
    """Reset gamma to an empty list."""

    if _counter != 0:
        raise ValueError(f"Fatal: non-zero counter: {_counter}")

    _gamma.clear()
