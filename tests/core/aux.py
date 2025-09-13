import lbd.term as term


def A(left: term.AST, right: term.AST) -> term.Application:
    return term.Application(left, right)


def F(body: term.AST) -> term.Abstraction:
    return term.Abstraction(body)


def N(index: int) -> term.Name:
    return term.Name(index)


IDENTITY = F(N(0))
FIRST = F(F(N(1)))
SECOND = F(F(N(0)))
