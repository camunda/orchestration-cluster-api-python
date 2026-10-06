from enum import StrEnum


class AdvancedGlobalListenerSourceFilterNeq(StrEnum):
    API = "API"
    CONFIGURATION = "CONFIGURATION"

    def __str__(self) -> str:
        return str(self.value)
