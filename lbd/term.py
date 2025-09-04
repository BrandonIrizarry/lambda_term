from dataclasses import dataclass, field


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
    depth: int
    freeness: int = field(init=False)

    def __post_init__(self):
        if self.index < 0:
            raise ValueError(f"Negative index: {self.index}")

        self.freeness = self.index - self.depth

    def __str__(self):
        if self.freeness < 0:
            return f"N({self.index}, {self.depth})"

        return f"G({self.freeness})"


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


# Keep this around for now, since some tests use it.
IDENTITY = Abstraction(Name(0, 1))
