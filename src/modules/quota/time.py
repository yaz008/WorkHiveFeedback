from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Hashable


@dataclass(slots=True)
class TimeQuota[T: Hashable]:
    __delta: timedelta
    __quota: int
    __members: dict[T, deque[datetime]]

    def __init__(self, delta: timedelta, quota: int) -> None:
        self.__delta = delta
        self.__quota = quota
        self.__members = defaultdict(deque)

    def exceeds(self, member: T) -> bool:
        now: datetime = datetime.now()
        self.__members[member].append(now)
        while (
            len(self.__members[member]) > 0
            and now - self.__members[member][0] > self.__delta
        ):
            self.__members[member].pop()
        return len(self.__members[member]) > self.__quota
