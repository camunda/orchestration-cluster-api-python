from enum import Enum


class ProcessDefinitionSearchQueryFilterState(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"

    def __str__(self) -> str:
        return str(self.value)
