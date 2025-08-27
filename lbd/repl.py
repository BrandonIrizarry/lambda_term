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

        # Here we support chaining multiple lambda terms on the same
        # line using ';' - useful, since we now support assignment as
        # a side-effect.
        ast = None
        i = 0
        buf: list[tkz.Token] = []

        while i < len(tokens):
            t = tokens[i]
            kind = t.kind

            if kind != tdef.Tk.SEMICOLON:
                buf.append(t)
            else:
                ast = evl.eval_tokens(buf)
                buf.clear()

            i += 1

        if len(buf) != 0:
            ast = evl.eval_tokens(buf)
            buf.clear()

        assert ast is not None

        # Back to our regularly scheduled program.
        if isinstance(ast, Exception):
            print(ast)
            continue

        print()
        print(ast)
        print()
        print(prettify.prettify(ast))
        print()
