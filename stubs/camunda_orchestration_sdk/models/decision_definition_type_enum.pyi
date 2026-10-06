from enum import StrEnum
class DecisionDefinitionTypeEnum(StrEnum):
    DECISION_TABLE = "DECISION_TABLE"
    LITERAL_EXPRESSION = "LITERAL_EXPRESSION"
    UNKNOWN = "UNKNOWN"
    UNSPECIFIED = "UNSPECIFIED"
    def __str__(self) -> str: ...
