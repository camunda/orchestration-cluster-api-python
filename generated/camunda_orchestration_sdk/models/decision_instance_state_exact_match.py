from enum import Enum


class DecisionInstanceStateExactMatch(str, Enum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
