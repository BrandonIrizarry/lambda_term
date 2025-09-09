from lbd.error import LambdaError
from lbd.evaluate import eval_line
from lbd.tokenize import tokenize


def load(filenames: list[str]) -> str | None:
    for filename in filenames:
        with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip()

                if line != "":
                    tokens = tokenize(line)

                    if isinstance(tokens, LambdaError):
                        return f"in '{filename}': {tokens}"

                    err = eval_line(tokens)

                    if isinstance(err, LambdaError):
                        return f"in '{filename}': {err}"
