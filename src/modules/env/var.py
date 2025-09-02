from os import getenv
from re import match

from typing_extensions import Self


class EnvVar(str):
    def __new__(cls: type[Self], name: str, pattern: str = r'.*') -> Self:
        var: str | None = getenv(key=name)
        if var is None:
            raise ValueError(f'Evnironment variable \"{name}\" is missing')
        if not match(fr'^{pattern}$', var):
            raise ValueError(
                f'Value of \"{name}\" must match the pattern r\"{pattern}\"'
            )
        return str.__new__(cls, var)
