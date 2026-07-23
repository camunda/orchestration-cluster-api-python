from enum import Enum

class PartitionState(str, Enum):
    ACTIVE = "active"
    JOINING = "joining"
    LEAVING = "leaving"
    RECOVERING = "recovering"
    UNKNOWN = "unknown"
    def __str__(self) -> str: ...
