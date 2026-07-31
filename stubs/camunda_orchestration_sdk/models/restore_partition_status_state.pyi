from enum import Enum

class RestorePartitionStatusState(str, Enum):
    PENDING = "PENDING"
    RESTORED = "RESTORED"
    RESTORING = "RESTORING"
    def __str__(self) -> str: ...
