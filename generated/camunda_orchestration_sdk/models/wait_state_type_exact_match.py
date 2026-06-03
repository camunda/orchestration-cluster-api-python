from enum import Enum


class WaitStateTypeExactMatch(str, Enum):
    JOB = "JOB"
    MESSAGE = "MESSAGE"

    def __str__(self) -> str:
        return str(self.value)
