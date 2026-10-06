from enum import StrEnum
class AdvancedBatchOperationItemStateFilterEq(StrEnum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    def __str__(self) -> str: ...
