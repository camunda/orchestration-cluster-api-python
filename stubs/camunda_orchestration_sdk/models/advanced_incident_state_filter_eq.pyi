from enum import Enum
class AdvancedIncidentStateFilterEq(str, Enum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"
    def __str__(self) -> str: ...
