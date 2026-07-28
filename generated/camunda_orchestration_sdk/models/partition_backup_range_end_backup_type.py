from enum import Enum


class PartitionBackupRangeEndBackupType(str, Enum):
    MANUAL_BACKUP = "MANUAL_BACKUP"
    SCHEDULED_BACKUP = "SCHEDULED_BACKUP"

    def __str__(self) -> str:
        return str(self.value)
