from enum import StrEnum


class AuditLogActorTypeExactMatch(StrEnum):
    ANONYMOUS = "ANONYMOUS"
    CLIENT = "CLIENT"
    UNKNOWN = "UNKNOWN"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)
