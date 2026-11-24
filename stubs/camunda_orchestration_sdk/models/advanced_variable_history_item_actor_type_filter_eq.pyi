from enum import Enum

class AdvancedVariableHistoryItemActorTypeFilterEq(str, Enum):
    CLIENT = "CLIENT"
    ENGINE = "ENGINE"
    UNKNOWN = "UNKNOWN"
    USER = "USER"
    def __str__(self) -> str: ...
