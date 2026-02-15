from enum import Enum
class AuditLogActorTypeEnum(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    CLIENT = "CLIENT"
    UNKNOWN = "UNKNOWN"
    USER = "USER"
    def __str__(self) -> str: ...
