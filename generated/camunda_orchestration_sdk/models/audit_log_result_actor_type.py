from enum import StrEnum


class AuditLogResultActorType(StrEnum):
    ANONYMOUS = "ANONYMOUS"
    CLIENT = "CLIENT"
    UNKNOWN = "UNKNOWN"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)
