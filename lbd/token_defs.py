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
    label: str
    regex: str
    is_dynamic: bool = False


class Tk(enum.Enum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    ASSIGN = TkEntry(enum.auto(), ":=", r":=")
    DEF = TkEntry(enum.auto(), "def", r"def\s")
    DOT = TkEntry(enum.auto(), ".", r"\.")
    LAMBDA = TkEntry(enum.auto(), "\\", r"\\")
    LEFT_PAREN = TkEntry(enum.auto(), "(", r"\(")
    RIGHT_PAREN = TkEntry(enum.auto(), ")", r"\)")
    SPACE = TkEntry(enum.auto(), "", r"[\t ]")
    NAME = TkEntry(enum.auto(), "", IDENTIFIER, True)
    ERROR = TkEntry(enum.auto(), "", r".", True)
