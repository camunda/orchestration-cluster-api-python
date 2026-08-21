from enum import Enum


class ClusterHistoryBackupTenantInfoClusterHistoryBackupTenantState(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    INCOMPATIBLE = "INCOMPATIBLE"
    INCOMPLETE = "INCOMPLETE"
    IN_PROGRESS = "IN_PROGRESS"
    NOT_FOUND = "NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
