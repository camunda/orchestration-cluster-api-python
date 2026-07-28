from enum import Enum


class Mode(str, Enum):
    PROCESSING = "PROCESSING"
    RECOVERING = "RECOVERING"

    def __str__(self) -> str:
        return str(self.value)
