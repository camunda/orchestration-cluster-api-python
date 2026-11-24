from enum import Enum


class VariableHistoryItemSearchQuerySortRequestField(str, Enum):
    VARIABLEHISTORYITEMKEY = "variableHistoryItemKey"

    def __str__(self) -> str:
        return str(self.value)
