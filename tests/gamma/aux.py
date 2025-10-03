import lbd.term as term


def A(left: term.AST, right: term.AST) -> term.Application:
    return term.Application(left, right)


def F(body: term.AST) -> term.Abstraction:
    return term.Abstraction(body)


def N(index: int, aux: int) -> term.Name:
    return term.Name(index, aux)


def G(index: int, depth: int) -> term.Name:
    """Return a new free name.

    By construction, INDEX is the given name's gamma value.

    """

    return term.Name(index + depth, depth)


def S(name: term.Name, value: term.AST) -> term.Assignment:
    return term.Assignment(name, value)


def E() -> term.Empty:
    return term.Empty()


IDENTITY = F(N(0, 1))
FIRST = F(F(N(1, 2)))
SECOND = F(F(N(0, 2)))
SELF_APPLY = F(A(N(0, 1), N(0, 1)))
APPLY = F(F(A(N(1, 2), N(0, 2))))
PAIR = F(F(F(A(A(N(0, 3),
                 N(2, 3)),
               N(1, 3)))))
