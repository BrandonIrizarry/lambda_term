class IncompleteTermError(Exception):
    pass


class TrailingGarbageError(Exception):
    pass


class UnboundNameError(Exception):
    def __init__(self, position, name):
        self.position = position
        self.name = name

    def __str__(self):
        return "Name '{}' at token-position {} is unbound"\
            .format(self.name, self.position)


class StrayTokenError(Exception):
    def __init__(self, position, token):
        self.position = position
        self.token = token

    def __str__(self):
        return "Stray token '{}' at token-position {}"\
            .format(self.token, self.position)


class AbstractionNoDotError(Exception):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return "Missing dot-separator at token-position {}"\
            .format(self.position)
