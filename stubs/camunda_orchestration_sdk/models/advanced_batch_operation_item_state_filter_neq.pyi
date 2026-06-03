from enum import Enum

class AdvancedBatchOperationItemStateFilterNeq(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    def __str__(self) -> str: ...
