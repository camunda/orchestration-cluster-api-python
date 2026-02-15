from enum import Enum
class AdvancedJobStateFilterNeq(str, Enum):
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    ERROR_THROWN = "ERROR_THROWN"
    FAILED = "FAILED"
    MIGRATED = "MIGRATED"
    RETRIES_UPDATED = "RETRIES_UPDATED"
    TIMED_OUT = "TIMED_OUT"
    def __str__(self) -> str: ...
