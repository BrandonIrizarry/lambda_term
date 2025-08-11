import re
import typing


class Status(typing.TypedDict):
    user_data: typing.Any
    error: str | None


def load_d(filename) -> Status:
    mobj = re.fullmatch(r"([^.]+)\.(\w+)", filename)

    if not mobj:
        return {"user_data": [], "error": f"Wrong format (possible missing extension): {filename}"}
    elif mobj.group(2) != "lbd":
        return {"user_data": [], "error": f"Non-lbd extension: {mobj.group(2)}"}

    lines = None

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

            return {"user_data": lines, "error": None}
    except FileNotFoundError:
        return {"user_data": [], "error": f"File not found: {filename}"}
