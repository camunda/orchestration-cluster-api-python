from enum import StrEnum
class DecisionInstanceStateEnum(StrEnum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    UNSPECIFIED = "UNSPECIFIED"
    def __str__(self) -> str: ...
