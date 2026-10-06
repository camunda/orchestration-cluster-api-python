from enum import StrEnum
class AdvancedIncidentStateFilterNeq(StrEnum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"
    def __str__(self) -> str: ...
