from enum import Enum

class AdvancedWaitStateTypeFilterNeq(str, Enum):
    JOB = "JOB"
    MESSAGE = "MESSAGE"
    def __str__(self) -> str: ...
