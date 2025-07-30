import readline
import os
import atexit

from beta import beta_reduce
from parse import parse


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
normally only for application terms.

Use backslash (\\) for the lambda symbol.

All lambda application terms must be explicitly parenthesized.

For example, for the self-application function, the correct form would
be \\x.(x x), not \\x.x x.
""")

while True:
    try:
        raw_term = input("> ")
        readline.add_history(raw_term)

        ast, _ = parse(raw_term)

        value = beta_reduce(ast)

        print()
        print(value)
    except EOFError:
        break
