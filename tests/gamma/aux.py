import lbd.term as term


def A(left: term.AST, right: term.AST) -> term.Application:
    return term.Application(left, right)


def F(body: term.AST) -> term.Abstraction:
    return term.Abstraction(body)


def N(index: int) -> term.Name:
    return term.Name(index)


def G(index: int, depth: int) -> term.Name:
    """Return a new free name.

    By construction, INDEX is the given name's gamma value.

    """

    return term.Name(index + depth)


def S(name: term.Name, value: term.AST) -> term.Assignment:
    return term.Assignment(name, value)


def E() -> term.Empty:
    return term.Empty()
