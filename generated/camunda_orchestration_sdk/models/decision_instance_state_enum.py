from enum import StrEnum


class DecisionInstanceStateEnum(StrEnum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    # deprecated since 8.9.0
    UNKNOWN = "UNKNOWN"
    # deprecated since 8.9.0
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
