from enum import StrEnum
class ProcessDefinitionFilterState(StrEnum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"
    def __str__(self) -> str: ...
