import readline
import os
import atexit
from wonderwords import RandomWord

from beta import beta_reduce
from parse import parse, Term


histfile = os.path.join(os.getcwd(), ".repl_history")

try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)


print("""
Welcome to the lambda REPL.

You can enter an lambda term at the prompt to see its result under
normal order beta reduction.

This works for all lambda terms, though the result is interesting
normally only for application terms. Upon evaluation, fresh names are
generated for local values, since the original ones are discarded due
to the use of DeBruijn indices to avoid name-clashes.

Use backslash (\\) for the lambda symbol.

All lambda application terms must be explicitly parenthesized.

For example, for the self-application function, the correct form would
be \\x.(x x), not \\x.x x.
""")

# Use this to generate ad-hoc local variable names (see docstring of
# 'pretty_print_term_ast'.)
rword = RandomWord()


def pretty_print_term_ast(ast, env):
    """Pretty print AST as a human-readable lambda expression.

    Since the AST is constructed using DeBruijn indices, the original
    local variable names are discarded, and so original names are used
    for the reconstructed human-readable expression.

    """

    if ast["kind"] == Term.NAME:
        # A depth of -1 corresponds to TOS, -2 t one underneath, etc.
        # Ex: index = 0 -> -1, index = 1 -> -2, etc.
        depth = -(ast["index"] + 1)

        print(env[depth], end="")
    elif ast["kind"] == Term.ABSTRACTION:
        # Generate a random word to use as the function parameter.
        param = rword.word()
        env.append(param)

        print("\\{}.".format(param), end="")
        pretty_print_term_ast(ast["body"], env[:])
    elif ast["kind"] == Term.APPLICATION:
        left = pretty_print_term_ast(ast["left"], env[:])
        right = pretty_print_term_ast(ast["right"], env[:])

        print("({} {})".format(left, right))


while True:
    try:
        raw_term = input("> ")
        readline.add_history(raw_term)

        ast, _ = parse(raw_term)

        value = beta_reduce(ast)

        print()
        pretty_print_term_ast(value, [])
        print()
    except EOFError:
        break
