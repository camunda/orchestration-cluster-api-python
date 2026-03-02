from enum import Enum


class AdvancedIncidentStateFilterEq(str, Enum):
    ACTIVE = "ACTIVE"
    MIGRATED = "MIGRATED"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

    def __str__(self) -> str:
        return str(self.value)
