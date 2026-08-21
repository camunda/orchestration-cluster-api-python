from enum import Enum


class ClusterRuntimeBackupTakeOutcome(str, Enum):
    FAILED = "FAILED"
    TRIGGERED = "TRIGGERED"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
