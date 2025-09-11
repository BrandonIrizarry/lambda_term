import enum
from dataclasses import dataclass


@dataclass
class Entry:
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

    ASSIGN = Entry(enum.auto(), ":=")
    DEF = Entry(enum.auto(), "def", True)
    DOT = Entry(enum.auto(), ".")
    ERROR = Entry(enum.auto(), "")
    LAMBDA = Entry(enum.auto(), "\\")
    LEFT_PAREN = Entry(enum.auto(), "(")
    NAME = Entry(enum.auto(), "")
    RIGHT_PAREN = Entry(enum.auto(), ")")
    SPACE = Entry(enum.auto(), "")
