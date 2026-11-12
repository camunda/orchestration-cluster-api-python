from enum import Enum


class DecisionDefinitionTypeEnum(str, Enum):
    """Contains deprecated members: ``UNSPECIFIED`` (since 8.9.0)."""

    DECISION_TABLE = "DECISION_TABLE"
    LITERAL_EXPRESSION = "LITERAL_EXPRESSION"
    UNKNOWN = "UNKNOWN"
    # deprecated since 8.9.0
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
