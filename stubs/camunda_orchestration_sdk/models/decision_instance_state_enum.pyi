from enum import Enum

class DecisionInstanceStateEnum(str, Enum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNSPECIFIED = "UNSPECIFIED"
    def __str__(self) -> str: ...
