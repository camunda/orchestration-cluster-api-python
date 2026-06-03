from enum import Enum
class ElementInstanceWaitStateResultWaitStateType(str, Enum):
    JOB = "JOB"
    MESSAGE = "MESSAGE"
    def __str__(self) -> str: ...
