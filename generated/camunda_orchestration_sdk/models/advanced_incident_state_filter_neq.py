from enum import Enum


class AdvancedIncidentStateFilterNeq(str, Enum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
