from enum import Enum

class AdvancedWaitStateTypeFilterEq(str, Enum):
    JOB = "JOB"
    MESSAGE = "MESSAGE"
    def __str__(self) -> str: ...
