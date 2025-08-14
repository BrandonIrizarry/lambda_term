import lbd.status as status


def eval_directive(name: str, params: list[str]) -> status.Status:
    match name:
        case "load":
            filename = params[0]
            return load_d(filename)
        case _:
            return {"user_data": [], "error": f"Undefined directive: '{name}'"}


def load_d(filename: str) -> status.Status:
    try:
        with open(filename, "r") as file:
            lines = []

            for _line in file.readlines():
                line = _line.strip()

                if line != "":
                    lines.append(line)

            return {"user_data": lines, "error": None}
    except FileNotFoundError:
        return {"user_data": [], "error": f"File not found: {filename}"}
