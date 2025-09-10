import enum


class Tk(enum.Enum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    ASSIGN = (enum.auto(), ":=")
    DEF = (enum.auto(), "def")
    DOT = (enum.auto(), ".")
    ERROR = (enum.auto(), "")
    LAMBDA = (enum.auto(), "\\")
    LEFT_PAREN = (enum.auto(), "(")
    NAME = (enum.auto(), "")
    RIGHT_PAREN = (enum.auto(), ")")
    SPACE = (enum.auto(), "")
