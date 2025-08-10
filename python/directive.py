import enum
import re


class Status(enum.Enum):
    SUCCESS = enum.auto()
    FILE_NOT_FOUND = enum.auto()
    WRONG_EXTENSION = enum.auto()


type program = list[str]


def load_d(filename) -> tuple[program, Status]:
    if not re.fullmatch(r"\S+\.lbd", filename):
        return ([], Status.WRONG_EXTENSION)

    lines = None

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

            return (lines, Status.SUCCESS)
    except FileNotFoundError:
        return ([], Status.FILE_NOT_FOUND)
