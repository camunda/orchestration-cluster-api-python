from enum import Enum

class CheckpointType(str, Enum):
    MANUAL_BACKUP = "MANUAL_BACKUP"
    MARKER = "MARKER"
    SCHEDULED_BACKUP = "SCHEDULED_BACKUP"
    def __str__(self) -> str: ...
