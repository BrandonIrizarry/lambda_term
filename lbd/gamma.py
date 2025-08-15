# For now, implement gamma as a list of free names, given as strings.
_gamma: list[str] = []


def gamma(free_name: str) -> int:
    """Return the index of FREE_NAME inside gamma.

    If not found, return -1.

    """

    try:
        index = _gamma.index(free_name)
    except ValueError:
        return -1

    return index


def add(free_name: str) -> None:
    """Add FREE_NAME to gamma."""

    _gamma.append(free_name)


def debruijn(free_name: str, offset: int) -> int:
    """Compute the effective DeBruijn index of FREE_NAME.

    OFFSET is meant to be the length of the current local, nameless
    environment kept track of by the parser.

    """

    index = gamma(free_name)

    if index == -1:
        add(free_name)
        index = gamma(free_name)

    return offset + index
