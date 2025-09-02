import atexit
import os
import readline

import lbd.error as err
import lbd.evaluate as evl
import lbd.prettify as prettify
import lbd.token_defs as tdef
import lbd.tokenize as tkz

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

        tokens = tkz.tokenize(repl_input)

        if isinstance(tokens, err.LambdaError):
            print(tokens)
            continue

        # 'eval_line' specifically supports chaining multiple lambda
        # terms on the same line using ';'.
        ast = evl.eval_line(tokens)

        if isinstance(ast, Exception):
            print(ast)
            continue

        print()
        print(ast)
        print()
        print(prettify.prettify(ast))
        print()
