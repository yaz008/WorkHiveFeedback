from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from telebot.types import Message


@dataclass(slots=True)
class PendingSet:
    on_error: Callable[[Message], Any]
    __users: set[int] = field(init=False)

    def add(self, user: int) -> None:
        self.__users.add(user)

    def remove(self, user: int) -> None:
        self.__users.remove(user)

    def assert_pending(
        self, func: Callable[[Message], None]
    ) -> Callable[[Message], None]:
        def wrapper(message: Message) -> None:
            if message.chat.id not in self.__users:
                self.on_error(message)
            else:
                func(message)
                self.remove(message.chat.id)

        return wrapper
