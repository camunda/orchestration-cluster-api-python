from enum import StrEnum
class BatchOperationStateEnum(StrEnum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    FAILED = "FAILED"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    SUSPENDED = "SUSPENDED"
    def __str__(self) -> str: ...
