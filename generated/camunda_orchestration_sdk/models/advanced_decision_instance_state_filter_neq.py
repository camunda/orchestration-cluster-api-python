from enum import StrEnum


class AdvancedDecisionInstanceStateFilterNeq(StrEnum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
