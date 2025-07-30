from beta import beta_reduce
from parse import parse

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
        ast, _ = parse(raw_term)

        value = beta_reduce(ast)

        print()
        print(value)
    except EOFError:
        break
