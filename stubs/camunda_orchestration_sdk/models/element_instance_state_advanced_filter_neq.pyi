from enum import Enum
class ElementInstanceStateAdvancedFilterNeq(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"
    def __str__(self) -> str: ...
