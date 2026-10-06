from enum import StrEnum


class AdvancedIncidentStateFilterEq(StrEnum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
