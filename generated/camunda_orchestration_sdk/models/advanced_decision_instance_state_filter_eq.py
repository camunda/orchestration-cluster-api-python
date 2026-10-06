from enum import StrEnum


class AdvancedDecisionInstanceStateFilterEq(StrEnum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
