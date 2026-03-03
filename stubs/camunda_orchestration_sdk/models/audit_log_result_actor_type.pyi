from enum import Enum
class AuditLogResultActorType(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    CLIENT = "CLIENT"
    UNKNOWN = "UNKNOWN"
    USER = "USER"
    def __str__(self) -> str: ...
