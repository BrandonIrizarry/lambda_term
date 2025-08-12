import re
import typing


class Status(typing.TypedDict):
    user_data: typing.Any
    error: str | None


def load_d(filename: str) -> Status:
    try:
        with open(f"{filename}.lbd", "r") as file:
            lines = []

            for _line in file.readlines():
                line = _line.strip()

                if line != "":
                    lines.append(line)

            return {"user_data": lines, "error": None}
    except FileNotFoundError:
        return {"user_data": [], "error": f"File not found: {filename}"}
