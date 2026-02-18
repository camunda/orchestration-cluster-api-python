from enum import Enum


class TenantFilterEnum(str, Enum):
    ASSIGNED = "ASSIGNED"
    PROVIDED = "PROVIDED"

    def __str__(self) -> str:
        return str(self.value)
