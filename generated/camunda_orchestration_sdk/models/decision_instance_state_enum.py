from enum import Enum


class DecisionInstanceStateEnum(str, Enum):
    """Contains deprecated members: ``UNSPECIFIED`` (since 8.9.0), ``UNKNOWN`` (since 8.9.0)."""

    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    # deprecated since 8.9.0
    UNKNOWN = "UNKNOWN"
    # deprecated since 8.9.0
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
