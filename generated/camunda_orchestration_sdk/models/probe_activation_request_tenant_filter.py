from enum import Enum


class ProbeActivationRequestTenantFilter(str, Enum):
    ASSIGNED = "ASSIGNED"
    PROVIDED = "PROVIDED"

    def __str__(self) -> str:
        return str(self.value)
