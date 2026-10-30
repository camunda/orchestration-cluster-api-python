from enum import Enum


class AdvancedProtectionModeFilterEq(str, Enum):
    REDACT = "REDACT"

    def __str__(self) -> str:
        return str(self.value)
