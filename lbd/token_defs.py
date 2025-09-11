import enum
from dataclasses import dataclass

IDENTIFIER = r"[A-Za-z_]\w*"


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
    name: str
    label: str
    regex: str


class Tk(enum.Enum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    ASSIGN = TkEntry(enum.auto(), "assign", ":=", r":=")
    DEF = TkEntry(enum.auto(), "def", "def", r"def")
    DOT = TkEntry(enum.auto(), "dot", ".", r"\.")
    ERROR = TkEntry(enum.auto(), "error", "", r".")
    LAMBDA = TkEntry(enum.auto(), "lambda", "\\", r"\\")
    LEFT_PAREN = TkEntry(enum.auto(), "left_paren", "(", r"\(")
    NAME = TkEntry(enum.auto(), "name", "", IDENTIFIER)
    RIGHT_PAREN = TkEntry(enum.auto(), "right_paren", ")", r"\)")
    SPACE = TkEntry(enum.auto(), "space", "", r"[\t ]")
