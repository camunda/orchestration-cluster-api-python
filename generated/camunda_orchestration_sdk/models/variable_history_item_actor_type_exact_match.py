from enum import Enum


class VariableHistoryItemActorTypeExactMatch(str, Enum):
    CLIENT = "CLIENT"
    ENGINE = "ENGINE"
    UNKNOWN = "UNKNOWN"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)
