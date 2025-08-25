import lbd.term as term


def A(left: term.AST, right: term.AST) -> term.Application:
    return term.Application(label=None, left=left, right=right)


def F(body: term.AST) -> term.Abstraction:
    return term.Abstraction(label=None, body=body)


def N(index: int, depth: int) -> term.Name:
    return term.Name(label=None, index=index, depth=depth)


def G(index: int, depth: int) -> term.Name:
    return term.Name(label=None, index=index + depth, depth=depth)
