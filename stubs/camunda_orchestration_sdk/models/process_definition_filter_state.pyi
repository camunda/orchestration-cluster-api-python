from enum import Enum
class ProcessDefinitionFilterState(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    def __str__(self) -> str: ...
