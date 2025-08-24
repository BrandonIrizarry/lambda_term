import enum
from typing import Any


class Term(enum.StrEnum):
    NAME = "name"
    ABSTRACTION = "abstraction"
    APPLICATION = "application"

    def __repr__(self):
        return self


type AST = dict[str, Any]


def new_name(index: int, depth: int) -> AST:
    """Construct and return a name with the given INDEX."""

    return {
        "kind": Term.NAME,
        "index": index,
        "depth": depth,
    }


def new_free_name(index: int, depth: int) -> AST:
    """Shortcut to define a free name.

    INDEX is passed down to new_name with an offset of DEPTH.

    """

    return new_name(index + depth, depth)


def freeness(name: AST) -> int:
    """For NAME, return index - depth.

    Local variables have a negative freeness, while free symbols have
    a non-negative freeness. For free symbols, their freeness value is
    their index into gamma.

    """

    return name["index"] - name["depth"]


def new_abstraction(body: AST) -> AST:
    """Construct and return an abstraction with the given BODY."""

    return {
        "kind": Term.ABSTRACTION,
        "body": body,
    }


def new_application(left: AST, right: AST) -> AST:
    """Construct and return an application with the given LEFT and
    RIGHT terms."""

    return {
        "kind": Term.APPLICATION,
        "left": left,
        "right": right,
    }
