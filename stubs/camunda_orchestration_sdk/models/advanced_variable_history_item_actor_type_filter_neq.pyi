from enum import Enum

class AdvancedVariableHistoryItemActorTypeFilterNeq(str, Enum):
    CLIENT = "CLIENT"
    ENGINE = "ENGINE"
    UNKNOWN = "UNKNOWN"
    USER = "USER"
    def __str__(self) -> str: ...
