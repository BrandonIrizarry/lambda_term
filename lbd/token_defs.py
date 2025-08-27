import enum


class Tk(enum.Enum):
    """An enum used to tag token types.

    Empty-string entries are special cases, handled separately.

    """

    LEFT_PAREN = (enum.auto(), "(")
    RIGHT_PAREN = (enum.auto(), ")")
    DOT = (enum.auto(), ".")
    LAMBDA = (enum.auto(), "\\")
    SYM = (enum.auto(), "sym")
    SPACE = (enum.auto(), "")
    NAME = (enum.auto(), "")
    ERROR = (enum.auto(), "")
    LEFT_ANGLE = (enum.auto(), "<")
    RIGHT_ANGLE = (enum.auto(), ">")
