from enum import Enum

class JobStateExactMatch(str, Enum):
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    ERROR_THROWN = "ERROR_THROWN"
    FAILED = "FAILED"
    MIGRATED = "MIGRATED"
    PRIORITY_UPDATED = "PRIORITY_UPDATED"
    RETRIES_UPDATED = "RETRIES_UPDATED"
    TIMED_OUT = "TIMED_OUT"
    def __str__(self) -> str: ...
