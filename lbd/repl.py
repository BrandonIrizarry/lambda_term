import atexit
import os
import readline

import lbd.evaluate as evl
import lbd.prettify as prettify
from lbd.error import LambdaError

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

        ast = evl.eval_raw_term(repl_input)

        if isinstance(ast, Exception):
            print(ast)
            continue

        print()

        pretty = prettify.prettify(ast)

        # Save the last evaluation result in '_', similar to how
        # Python does. Note that we can use Lambda Term itself to
        # achieve this, via an assignment expression.
        err = evl.eval_raw_term(f"def _ := {pretty.lower()}")

        if isinstance(err, LambdaError):
            raise ValueError(f"Fatal: '_' feature broken: {err}")

        print(ast)
        print(pretty)
        print()
