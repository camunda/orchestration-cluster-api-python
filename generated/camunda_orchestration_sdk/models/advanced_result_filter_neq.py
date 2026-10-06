from enum import StrEnum


class AdvancedResultFilterNeq(StrEnum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"

    def __str__(self) -> str:
        return str(self.value)
