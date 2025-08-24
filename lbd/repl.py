import atexit
import os
import readline

from wonderwords import RandomWord

import lbd.evaluate as evl
import lbd.gamma as g
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


def prettify(ast: term.AST, env: list[str]) -> str:
    """Create a human-readable lambda expression from AST.

    Since the AST is constructed using DeBruijn indices, the original
    local variable names are discarded, and so synthetic names are used
    for the reconstructed human-readable expression.

    Return the prettified version of AST as a string.

    """

    match ast["kind"]:
        case term.Term.NAME:
            fness = term.freeness(ast)

            if fness < 0:
                # An env_depth of -1 corresponds to TOS, -2 t one underneath, etc.
                # Ex: index = 0 -> -1, index = 1 -> -2, etc.
                idx = ast["index"]
                env_depth = -(idx + 1)

                return env[env_depth]
            else:
                free_sym = g.sym_get(fness)

                if free_sym is None:
                    raise ValueError(f"Fatal: sym_get({fness}) failed")

                return free_sym.label.upper()

        case term.Term.ABSTRACTION:
            # Generate a random word to use as the function parameter.
            param: str = rword.word()
            env.append(param)

            body = prettify(ast["body"], env[:])
            return f"\\{param}.{body}"

        case term.Term.APPLICATION:
            left = prettify(ast["left"], env[:])
            right = prettify(ast["right"], env[:])

            return f"({left} {right})"


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
        print(prettify(ast, []))
        print()
