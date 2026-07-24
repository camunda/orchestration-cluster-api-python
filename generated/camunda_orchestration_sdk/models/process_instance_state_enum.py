from enum import Enum


class ProcessInstanceStateEnum(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"

    def __str__(self) -> str:
        return str(self.value)
