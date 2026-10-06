from enum import StrEnum
class ElementInstanceResultState(StrEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"
    def __str__(self) -> str: ...
