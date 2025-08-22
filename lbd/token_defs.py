import enum


class Tk(enum.Enum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    ASSIGN = (enum.auto(), ":=")
    LEFT_PAREN = (enum.auto(), "(")
    RIGHT_PAREN = (enum.auto(), ")")
    DOT = (enum.auto(), ".")
    LAMBDA = (enum.auto(), "\\")
    DEF = (enum.auto(), "def")
    SYM = (enum.auto(), "sym")
    SPACE = (enum.auto(), "")
    NAME = (enum.auto(), "")
    ERROR = (enum.auto(), "")
    SET = (enum.auto(), "set")
