from enum import Enum
class IncidentStateExactMatch(str, Enum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"
    def __str__(self) -> str: ...
