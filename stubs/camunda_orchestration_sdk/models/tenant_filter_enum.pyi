from enum import StrEnum
class TenantFilterEnum(StrEnum):
    ASSIGNED = "ASSIGNED"
    PROVIDED = "PROVIDED"
    def __str__(self) -> str: ...
