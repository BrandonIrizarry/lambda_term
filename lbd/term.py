from dataclasses import dataclass


@dataclass
class AST():
    pass


@dataclass
class Empty(AST):
    def __str__(self):
        return "nil"


@dataclass
class Name(AST):
    index: int

    def __post_init__(self):
        if self.index < 0:
            raise ValueError(f"Negative index: {self.index}")

    def __str__(self):
        return f"N({self.index})"


@dataclass
class Abstraction(AST):
    body: AST

    def __str__(self):
        return f"F({self.body})"


@dataclass
class Application(AST):
    left: AST
    right: AST

    def __str__(self):
        return f"A({self.left} {self.right})"


@dataclass
class Assignment(AST):
    name: Name
    value: AST

    def __str__(self):
        return f"<{self.name}, {self.value}>"


# Define convenient aliases.
#
# Since I use these all the time in the tests, I've gotten used to
# them as standard terminology.
N = Name
F = Abstraction
A = Application

# Keep this around for now, since some tests use it.
IDENTITY = F(N(0))

# The Y combinator, used to define 'letrec'.
#
# \f.(\s.(f (s s)) \s.(f (s s)))
#
RECURSIVE = F(A(F(A(N(1),
                    A(N(0),
                      N(0)))),
                F(A(N(1),
                    A(N(0),
                      N(0))))))
