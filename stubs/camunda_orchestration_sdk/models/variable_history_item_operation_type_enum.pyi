from enum import Enum

class VariableHistoryItemOperationTypeEnum(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    def __str__(self) -> str: ...
