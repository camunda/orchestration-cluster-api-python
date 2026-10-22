from enum import Enum

class ProtectionModeExactMatch(str, Enum):
    REDACT = "REDACT"
    def __str__(self) -> str: ...
