import lbd.error as err


def eval_directive(name: str, params: list[str]) -> list[str] | err.LambdaError:
    match name:
        case "load":
            filename = params[0]
            return load_d(filename)
        case _:
            raise ValueError(f"Undefined directive: '{name}'")


def load_d(filename: str) -> list[str] | err.LambdaError:
    try:
        with open(filename, "r") as file:
            lines = []

            for _line in file.readlines():
                line = _line.strip()

                if line != "":
                    lines.append(line)

            return lines
    except FileNotFoundError:
        raise ValueError(f"File not found: {filename}")
