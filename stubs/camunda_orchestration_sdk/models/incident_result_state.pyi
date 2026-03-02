from enum import Enum
class IncidentResultState(str, Enum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    def __str__(self) -> str: ...
