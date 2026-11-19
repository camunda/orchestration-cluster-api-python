from enum import Enum

class ProcessDefinitionSearchQueryFilterState(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"
    SUSPENDED = "SUSPENDED"
    def __str__(self) -> str: ...
