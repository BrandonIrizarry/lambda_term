

def eval_directive(name: str, params: list[str]) -> list[str] | Exception:
    match name:
        case "load":
            filename = params[0]
            return load_d(filename)
        case _:
            return ValueError(f"Undefined directive: '{name}'")


def load_d(filename: str) -> list[str] | Exception:
    try:
        with open(filename, "r") as file:
            lines = []

            for _line in file.readlines():
                line = _line.strip()

                if line != "":
                    lines.append(line)

            return lines
    except FileNotFoundError:
        return ValueError(f"File not found: {filename}")
