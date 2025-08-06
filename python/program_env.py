import beta
import parse


class ProgramEnv():
    def __init__(self):
        self.env = dict()
        self.program = []

    def load_program(self, program):
        """Load PROGRAM as a list of statements or expressions to be
        evaluated later.

        In practice, these likely will be all def-statements, because
        any line before the last one is only useful for its
        side-effects.

        """

        self.program.extend(program)

    def append_line(self, line):
        """Append LINE to the end of SELF.PROGRAM.

        """

        self.program.append(line)

    def __evaluate(self, raw_term):
        ast, _, label = parse.parse(raw_term, self.env)

        # If we parsed a def-statement, associate the label with the
        # AST.
        if label is not None:
            self.env[label] = {
                "kind": beta.Term.NAME,
                "def": ast
            }

        return beta.beta_reduce(ast)

    def __substitute_globals(self, ast):
        # Be sure to return the modified AST.
        if ast["kind"] == beta.Term.NAME:
            if "def" in ast:
                ast = ast["def"]

            return ast
        elif ast["kind"] == beta.Term.ABSTRACTION:
            new_body = self.__substitute_globals(ast["body"])

            return parse.new_abstraction(new_body)
        elif ast["kind"] == beta.Term.APPLICATION:
            new_left = self.__substitute_globals(ast["left"])
            new_right = self.__substitute_globals(ast["right"])

            return parse.new_application(new_left, new_right)

    def run(self):
        """Run the currently loaded program, returning the last
        evaluation (an AST).

        If no program is loaded, return.

        """

        value = None

        for line in self.program:
            value = self.__evaluate(line)

        # Return the last evaluation, similar to Lisp.
        #
        # Note that, for the time being, if a program is empty, None
        # is returned.
        return value

    def eval_last(self):
        """Evaluate the last statement of the program only.

        This is mainly useful for the REPL, where statements are
        executed incrementally.

        """

        if len(self.program) == 0:
            return None

        return self.__evaluate(self.program[-1])
