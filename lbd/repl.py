import atexit
import os
import readline

from wonderwords import RandomWord

import lbd.evaluate as evl
import lbd.term as term

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

See the TUTORIAL file accompanying this project for details.

""")

# Use this to generate ad-hoc local variable names (see docstring of
# 'pretty_print_term_ast'.)
rword = RandomWord()


def pretty_print_term_ast(ast, env):
    """Pretty print AST as a human-readable lambda expression.

    Since the AST is constructed using DeBruijn indices, the original
    local variable names are discarded, and so synthetic names are used
    for the reconstructed human-readable expression.

    """

    if ast["kind"] == term.Term.NAME:
        # A depth of -1 corresponds to TOS, -2 t one underneath, etc.
        # Ex: index = 0 -> -1, index = 1 -> -2, etc.
        depth = -(ast["index"] + 1)

        print(env[depth], end="")
    elif ast["kind"] == term.Term.ABSTRACTION:
        # Generate a random word to use as the function parameter.
        param = rword.word()
        env.append(param)

        print("\\{}.".format(param), end="")
        pretty_print_term_ast(ast["body"], env[:])
    elif ast["kind"] == term.Term.APPLICATION:
        print("(", end="")
        pretty_print_term_ast(ast["left"], env[:])
        print(" ", end="")
        pretty_print_term_ast(ast["right"], env[:])
        print(")")


def repl():
    while True:
        try:
            repl_input = input("> ")
        except EOFError:
            break

        if repl_input == "":
            continue

        readline.add_history(repl_input)

        ast = evl.eval_raw_term(repl_input)

        if isinstance(ast, Exception):
            print(ast)
            continue

        print(ast)
