from enum import StrEnum
class AdvancedBatchOperationItemStateFilterNeq(StrEnum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    def __str__(self) -> str: ...
