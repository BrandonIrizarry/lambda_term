import re
import typing


class Status(typing.TypedDict):
    user_data: typing.Any
    error: str | None


def load_d(filename) -> Status:
    if not re.fullmatch(r"\S+\.lbd", filename):
        return {"user_data": [], "error": "Wrong extension"}

    lines = None

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

            return {"user_data": lines, "error": None}
    except FileNotFoundError:
        return {"user_data": [], "error": "file not found"}
