from enum import StrEnum
class AuditLogResultEnum(StrEnum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"
    def __str__(self) -> str: ...
