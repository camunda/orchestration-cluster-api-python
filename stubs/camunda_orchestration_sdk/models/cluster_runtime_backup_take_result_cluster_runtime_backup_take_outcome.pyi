from enum import Enum

class ClusterRuntimeBackupTakeResultClusterRuntimeBackupTakeOutcome(str, Enum):
    FAILED = "FAILED"
    TRIGGERED = "TRIGGERED"
    UNKNOWN = "UNKNOWN"
    def __str__(self) -> str: ...
