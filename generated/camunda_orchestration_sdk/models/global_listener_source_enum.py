from enum import StrEnum


class GlobalListenerSourceEnum(StrEnum):
    API = "API"
    CONFIGURATION = "CONFIGURATION"

    def __str__(self) -> str:
        return str(self.value)
