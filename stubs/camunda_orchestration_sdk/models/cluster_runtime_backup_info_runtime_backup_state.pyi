from enum import Enum

class ClusterRuntimeBackupInfoRuntimeBackupState(str, Enum):
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"
    DOES_NOT_EXIST = "DOES_NOT_EXIST"
    FAILED = "FAILED"
    INCOMPLETE = "INCOMPLETE"
    IN_PROGRESS = "IN_PROGRESS"
    def __str__(self) -> str: ...
