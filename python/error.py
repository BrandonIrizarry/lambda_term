class ParseError(Exception):
    def __init__(self, position, token):
        self.position = position
        self.token = token
        self.diagnostic = self.generate_diagnostic()
        print(self.diagnostic)

    @classmethod
    def set_tokens(cls, tokens):
        cls.tokens = tokens

    def generate_diagnostic(self):
        """Signify where in the user's expression a syntax error
        occurred.

        """

        current_tokens = self.tokens
        current_tokens.insert(self.position, "*")
        return "".join(current_tokens)


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


class IllegalTokenError(Exception):
    """Catch errors at the tokenizing stage.

    Since these always occur before the parsing stage, we can't
    inherit from ParseError.

    """

    def __init__(self, position, token):
        self.position = position
        self.token = token

    def __str__(self):
        return f"Illegal token {self.token} at token-position {self.position}"


class AbstractionNoDotError(ParseError):
    def __str__(self):
        return f"Missing dot-separator at token-position {self.position}"
