from enum import Enum


class DecisionDefinitionTypeEnum(str, Enum):
    DECISION_TABLE = "DECISION_TABLE"
    LITERAL_EXPRESSION = "LITERAL_EXPRESSION"
    UNKNOWN = "UNKNOWN"
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return str(self.value)
