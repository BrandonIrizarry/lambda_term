import atexit
import os
import readline

import lbd.evaluate as evl
import lbd.prettify as prettify

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
        print(prettify.prettify(ast))
        print()
