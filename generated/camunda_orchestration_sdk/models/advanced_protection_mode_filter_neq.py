from enum import Enum


class AdvancedProtectionModeFilterNeq(str, Enum):
    REDACT = "REDACT"

    def __str__(self) -> str:
        return str(self.value)
