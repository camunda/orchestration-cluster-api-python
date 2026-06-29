from enum import Enum


class WaitStateTypeEnum(str, Enum):
    CONDITION = "CONDITION"
    JOB = "JOB"
    MESSAGE = "MESSAGE"
    SIGNAL = "SIGNAL"
    TIMER = "TIMER"
    USER_TASK = "USER_TASK"

    def __str__(self) -> str:
        return str(self.value)
