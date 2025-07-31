class ParseError(Exception):
    def __init__(self, position, token):
        self.position = position
        self.token = token


class IncompleteTermError(ParseError):
    def __str__(self):
        return "Incomplete term"


class TrailingGarbageError(ParseError):
    def __str__(self):
        return "Trailing garbage"


class UnboundNameError(ParseError):
    def __str__(self):
        return f"Name '{self.token}' at token-position {self.position}\
        is unbound"


class StrayTokenError(ParseError):
    def __str__(self):
        return f"Stray token {self.token} at token-position {self.position}"


class AbstractionNoDotError(ParseError):
    def __str__(self):
        return f"Missing dot-separator at token-position {self.position}"
