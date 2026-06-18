from enum import Enum

class AdvancedWaitStateTypeFilterNeq(str, Enum):
    JOB = "JOB"
    MESSAGE = "MESSAGE"
    SIGNAL = "SIGNAL"
    TIMER = "TIMER"
    USER_TASK = "USER_TASK"
    def __str__(self) -> str: ...
