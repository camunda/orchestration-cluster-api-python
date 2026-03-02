from enum import Enum


class AdvancedDecisionInstanceStateFilterEq(str, Enum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
