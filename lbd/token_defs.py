import enum


class Tk(enum.Enum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    DOT = (enum.auto(), ".")
    ERROR = (enum.auto(), "")
    LAMBDA = (enum.auto(), "\\")
    LEFT_ANGLE = (enum.auto(), "<")
    LEFT_PAREN = (enum.auto(), "(")
    NAME = (enum.auto(), "")
    RIGHT_ANGLE = (enum.auto(), ">")
    RIGHT_PAREN = (enum.auto(), ")")
    SEMICOLON = (enum.auto(), ";")
    SPACE = (enum.auto(), "")
