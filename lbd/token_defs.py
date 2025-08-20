import enum


class Tk(enum.StrEnum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    ASSIGN = ":="
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    DOT = "."
    LAMBDA = "\\"
    DEF = "def"
    SYM = "sym"
    SPACE = ""
    NAME = ""
    ERROR = ""
