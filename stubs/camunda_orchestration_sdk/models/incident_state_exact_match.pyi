from enum import StrEnum
class IncidentStateExactMatch(StrEnum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"
    def __str__(self) -> str: ...
