from enum import Enum


class SearchUserTaskAuditLogsDataSortItemField(str, Enum):
    OPERATIONTYPE = "operationType"
    RESULT = "result"
    TIMESTAMP = "timestamp"

    def __str__(self) -> str:
        return str(self.value)
