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
        return "Name '{}' at token-position {} is unbound"\
            .format(self.name, self.position)


class StrayTokenError(ParseError):
    def __str__(self):
        return "Stray token '{}' at token-position {}"\
            .format(self.token, self.position)


class AbstractionNoDotError(ParseError):
    def __str__(self):
        return "Missing dot-separator at token-position {}"\
            .format(self.position)
