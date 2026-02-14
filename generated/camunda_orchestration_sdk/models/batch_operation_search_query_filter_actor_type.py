from enum import Enum


class BatchOperationSearchQueryFilterActorType(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    CLIENT = "CLIENT"
    UNKNOWN = "UNKNOWN"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)
