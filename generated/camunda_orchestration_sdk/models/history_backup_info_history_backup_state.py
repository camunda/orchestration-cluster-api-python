from enum import Enum


class HistoryBackupInfoHistoryBackupState(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    INCOMPATIBLE = "INCOMPATIBLE"
    INCOMPLETE = "INCOMPLETE"
    IN_PROGRESS = "IN_PROGRESS"

    def __str__(self) -> str:
        return str(self.value)
