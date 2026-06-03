from enum import Enum
class AuditLogResultEnum(str, Enum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"
    def __str__(self) -> str: ...
