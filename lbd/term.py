from dataclasses import dataclass


@dataclass(kw_only=True)
class AST():
    label: str | None = None


@dataclass
class Name(AST):
    index: int
    depth: int

    def freeness(self) -> int:
        """For NAME, return index - depth.

        Local variables have a negative freeness, while free symbols have
        a non-negative freeness. For free symbols, their freeness value is
        their index into gamma.

        """

        return self.index - self.depth


@dataclass
class Abstraction(AST):
    body: AST


@dataclass
class Application(AST):
    left: AST
    right: AST
