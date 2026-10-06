from enum import StrEnum


class AdvancedProcessInstanceStateFilterEq(StrEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"

    def __str__(self) -> str:
        return str(self.value)
