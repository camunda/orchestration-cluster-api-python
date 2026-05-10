from enum import Enum

class BatchOperationItemStateEnum(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    def __str__(self) -> str: ...
