import enum
from dataclasses import dataclass


@dataclass
class TkEntry:
    """A Tk entry.

    INDEX: used by the enum to uniquify entries.

    LABEL: what the token looks like in source code.

    Some tokens have their labels set to the empty string, since they
    are eventually associated with dynamically set values.

    IS_KEYWORD: whether this entry is associated with a keyword, for
    example 'DEF'.

    """

    index: int
    label: str
    is_keyword: bool = False


class Tk(enum.Enum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    ASSIGN = TkEntry(enum.auto(), ":=")
    DEF = TkEntry(enum.auto(), "def", True)
    DOT = TkEntry(enum.auto(), ".")
    ERROR = TkEntry(enum.auto(), "")
    LAMBDA = TkEntry(enum.auto(), "\\")
    LEFT_PAREN = TkEntry(enum.auto(), "(")
    NAME = TkEntry(enum.auto(), "")
    RIGHT_PAREN = TkEntry(enum.auto(), ")")
    SPACE = TkEntry(enum.auto(), "")
