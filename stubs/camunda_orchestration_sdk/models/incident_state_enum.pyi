from enum import Enum
class IncidentStateEnum(str, Enum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    def __str__(self) -> str: ...
