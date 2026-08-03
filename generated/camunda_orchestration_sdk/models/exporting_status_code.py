from enum import Enum


class ExportingStatusCode(str, Enum):
    EXPORTING = "EXPORTING"
    MIXED = "MIXED"
    PAUSED = "PAUSED"
    SOFT_PAUSED = "SOFT_PAUSED"

    def __str__(self) -> str:
        return str(self.value)
