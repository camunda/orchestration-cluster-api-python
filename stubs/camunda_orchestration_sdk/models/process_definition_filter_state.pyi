from enum import Enum

class ProcessDefinitionFilterState(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"
    def __str__(self) -> str: ...
