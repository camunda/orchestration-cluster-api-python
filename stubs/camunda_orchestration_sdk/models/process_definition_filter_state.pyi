from enum import Enum

class ProcessDefinitionFilterState(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"
    SUSPENDED = "SUSPENDED"
    def __str__(self) -> str: ...
