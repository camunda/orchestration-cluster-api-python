from enum import StrEnum


class ProcessDefinitionResultState(StrEnum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"

    def __str__(self) -> str:
        return str(self.value)
