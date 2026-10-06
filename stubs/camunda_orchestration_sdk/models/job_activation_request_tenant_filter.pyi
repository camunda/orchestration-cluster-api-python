from enum import StrEnum
class JobActivationRequestTenantFilter(StrEnum):
    ASSIGNED = "ASSIGNED"
    PROVIDED = "PROVIDED"
    def __str__(self) -> str: ...
