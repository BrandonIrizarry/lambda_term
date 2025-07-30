from beta import beta_reduce
from parse import parse

while True:
    try:
        raw_term = input("> ")
        ast, _ = parse(raw_term)

        value = beta_reduce(ast)
        print(value)
    except EOFError:
        break
