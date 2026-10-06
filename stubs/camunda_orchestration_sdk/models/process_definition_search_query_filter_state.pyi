from enum import StrEnum
class ProcessDefinitionSearchQueryFilterState(StrEnum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"
    def __str__(self) -> str: ...
