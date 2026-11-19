from enum import Enum

class ProcessDefinitionResultState(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DRAINING = "DRAINING"
    SUSPENDED = "SUSPENDED"
    def __str__(self) -> str: ...
