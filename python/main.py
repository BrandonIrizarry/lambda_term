import sys, enum

class Term(enum.StrEnum):
    NAME = "name"
    ABSTRACTION = "abstraction"
    APPLICATION = "application"

    def __repr__(self):
        return self

def new_name(index):
    """Construct and return a name with the given INDEX."""
    
    return {
        "kind": Term.NAME,
        "index": index,
    }


def new_abstraction(body):
    """Construct and return an abstraction with the given BODY."""
    
    return {
        "kind": Term.ABSTRACTION,
        "body": body,
    }


def new_application(left, right):
    """Construct and return an application with the given LEFT and RIGHT terms."""

    return {
        "kind": Term.APPLICATION,
        "left": left,
        "right": right,
    }


# The trick is to parse a string such as:
# ((\x.\y.(y x) \p.\q.p) \i.i)
# and end up with:
#

result = new_application(new_abstraction(new_abstraction(new_application(new_name(0),
                                                                         new_name(1)))),
                         new_abstraction(new_name(0)))


print(result)
