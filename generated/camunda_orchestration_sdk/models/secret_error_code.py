from enum import Enum


class SecretErrorCode(str, Enum):
    ACCESS_DENIED = "ACCESS_DENIED"
    INVALID_REFERENCE = "INVALID_REFERENCE"
    NOT_FOUND = "NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
