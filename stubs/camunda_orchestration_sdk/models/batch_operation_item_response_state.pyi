from enum import StrEnum
class BatchOperationItemResponseState(StrEnum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    def __str__(self) -> str: ...
