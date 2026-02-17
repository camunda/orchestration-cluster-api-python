from enum import Enum


class JobActivationRequestTenantFilter(str, Enum):
    ASSIGNED = "ASSIGNED"
    PROVIDED = "PROVIDED"

    def __str__(self) -> str:
        return str(self.value)
