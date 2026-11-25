from enum import Enum


class VariableHistoryItemOperationTypeExactMatch(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"

    def __str__(self) -> str:
        return str(self.value)
