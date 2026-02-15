from enum import Enum
class ElementInstanceStateAdvancedFilterEq(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"
    def __str__(self) -> str: ...
