from enum import Enum

class ClusterUpgradeStatusResponseStatus(str, Enum):
    MIGRATED = "MIGRATED"
    MIGRATION_IN_PROGRESS = "MIGRATION_IN_PROGRESS"
    UNKNOWN = "UNKNOWN"
    def __str__(self) -> str: ...
