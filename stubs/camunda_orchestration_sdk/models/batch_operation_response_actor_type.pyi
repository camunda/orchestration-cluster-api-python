from enum import StrEnum
class BatchOperationResponseActorType(StrEnum):
    ANONYMOUS = "ANONYMOUS"
    CLIENT = "CLIENT"
    UNKNOWN = "UNKNOWN"
    USER = "USER"
    def __str__(self) -> str: ...
