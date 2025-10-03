from dataclasses import dataclass

import lbd.gamma as gamma


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
    aux: int

    def __post_init__(self):
        if self.index < 0:
            raise ValueError(f"Negative index: {self.index}")

    def __str__(self):
        global_idx = self.index - self.aux

        if global_idx < 0:
            return f"N({self.index}, {self.aux})"

        return f"G({self.index},{self.aux}: {global_idx})"


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


def bind(global_name: str, term: AST) -> Abstraction:
    target_index = gamma.gamma(global_name)

    if target_index is None:
        raise ValueError(f"Fatal: non-global name {global_name}")

    def rec(term: AST, depth: int) -> None:
        match term:
            case Name():
                # 'idx' is the index into gamma. If it's equal to the
                # target index, we've found an instance of the global
                # variable we wish to bind. If global (i.e. idx >= 0),
                # we still need to increment its index because we're
                # going to wrap the whole expression in an
                # abstraction, and so need to preserve the invariant
                # INDEX - DEPTH == GAMMA.
                idx = term.index - depth
                term.aux += 1

                if idx == target_index:
                    term.index = depth
                elif idx >= 0:
                    term.index += 1

            case Abstraction():
                rec(term.body, depth + 1)

            case Application():
                rec(term.left, depth)
                rec(term.right, depth)

            case Assignment():
                rec(term.name, depth)
                rec(term.value, depth)

            case Empty():
                pass

    rec(term, 0)

    return Abstraction(term)


# Aliases.
N = Name
F = Abstraction
A = Application

# Keep this around for now, since some tests use it.
IDENTITY = F(N(0, 1))

# Y combinator.
#
# Note that, for 'inner', the N(1, 2) will refer to the outer 'F' in the
# definition of RECURSIVE. In general, the depth here is 2.

inner = F(A(N(1, 2),
            A(N(0, 2),
              N(0, 2))))

RECURSIVE = F(A(inner, inner))
