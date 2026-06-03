from enum import Enum
class WaitStateTypeEnum(str, Enum):
    JOB = "JOB"
    MESSAGE = "MESSAGE"
    def __str__(self) -> str: ...
