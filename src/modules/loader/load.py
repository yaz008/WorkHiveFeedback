from functools import cache
from json import load
from typing import Any


@cache
def load_text(path: str) -> str:
    with open(file=path, mode='r', encoding='UTF-8') as text_file:
        return text_file.read()


@cache
def load_json(path: str) -> Any:
    with open(file=path, mode='r', encoding='UTF-8') as json_file:
        return load(json_file)
