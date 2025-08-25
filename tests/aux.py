import lbd.term as term


def A(left: term.AST, right: term.AST) -> term.Application:
    return term.Application(left, right)


def F(body: term.AST) -> term.Abstraction:
    return term.Abstraction(body)


def N(index: int, depth: int) -> term.Name:
    return term.Name(index, depth)


def G(index: int, depth: int) -> term.Name:
    return term.Name(index + depth, depth)
