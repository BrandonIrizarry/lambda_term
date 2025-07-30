from beta import beta_reduce

while True:
    try:
        raw_term = input("> ")

        print(raw_term)
    except EOFError:
        break
