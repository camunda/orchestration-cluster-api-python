from enum import StrEnum
class AuditLogResultExactMatch(StrEnum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"
    def __str__(self) -> str: ...
