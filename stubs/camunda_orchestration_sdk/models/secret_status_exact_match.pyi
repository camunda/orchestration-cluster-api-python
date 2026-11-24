from enum import Enum

class SecretStatusExactMatch(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    EXPIRED = "EXPIRED"
    NOT_YET_ACTIVE = "NOT_YET_ACTIVE"
    def __str__(self) -> str: ...
