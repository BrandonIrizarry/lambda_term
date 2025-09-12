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
    is_keyword: bool = False


class Tk(enum.Enum):
    """An enum used to tag token types.

    Dynamic members are flagged by setting IS_DYNAMIC to True.

    A dynamic member is one which can be associated with a different
    value with each instance of the given token, for example a
    Tk.NAME, which is used for identifiers.

    """

    ASSIGN = TkEntry(enum.auto(), ":=", r":=")
    DEF = TkEntry(enum.auto(), "def", r"def\s", is_keyword=True)
    DOT = TkEntry(enum.auto(), ".", r"\.")
    LAMBDA = TkEntry(enum.auto(), "\\", r"\\")
    LEFT_PAREN = TkEntry(enum.auto(), "(", r"\(")
    RIGHT_PAREN = TkEntry(enum.auto(), ")", r"\)")
    LET = TkEntry(enum.auto(), "let", r"let\s", is_keyword=True)
    IN = TkEntry(enum.auto(), "in", r"in\s", is_keyword=True)

    # The following entries must occur at the end, since the main
    # tokenization regex defines tokens according to the order of the
    # entries in this enum.
    SPACE = TkEntry(enum.auto(), "", r"[\t ]")
    NAME = TkEntry(enum.auto(), "", IDENTIFIER, is_dynamic=True)
    ERROR = TkEntry(enum.auto(), "", r".", is_dynamic=True)


# Keep track of which Tk members are keywords.
#
# This is used later to flag keywords used in illegal positions, such
# as parameter names. Such usage can sometimes ostensibly make sense,
# but in the end is prone to causing confusion, e.g. '\def.def'.
#
# The tokenizer currently sees 'def', and since it doesn't match
# r'def\s', it accepts 'def' as a name token. However, the idea is to
# swap out this bogus name token for the _real_ 'def' token, so that
# the parser can flag it later (e.g. with an ILLEGAL_PARAM error.)

keywords: set[str] = {tk.value.label for tk in Tk if tk.value.is_keyword}
