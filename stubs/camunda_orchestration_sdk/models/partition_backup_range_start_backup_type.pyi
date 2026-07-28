from enum import Enum

class PartitionBackupRangeStartBackupType(str, Enum):
    MANUAL_BACKUP = "MANUAL_BACKUP"
    SCHEDULED_BACKUP = "SCHEDULED_BACKUP"
    def __str__(self) -> str: ...
