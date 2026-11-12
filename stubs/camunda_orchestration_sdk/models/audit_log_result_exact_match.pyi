from enum import Enum
class AuditLogResultExactMatch(str, Enum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"
    def __str__(self) -> str: ...
