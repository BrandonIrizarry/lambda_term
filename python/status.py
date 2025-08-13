import typing


class Status(typing.TypedDict):
    user_data: typing.Any
    error: str | None
