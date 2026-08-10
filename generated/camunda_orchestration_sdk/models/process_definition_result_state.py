from enum import Enum


class ProcessDefinitionResultState(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"

    def __str__(self) -> str:
        return str(self.value)
