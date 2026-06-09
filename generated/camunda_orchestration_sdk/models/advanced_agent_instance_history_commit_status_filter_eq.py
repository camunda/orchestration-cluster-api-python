from enum import Enum


class AdvancedAgentInstanceHistoryCommitStatusFilterEq(str, Enum):
    COMMITTED = "COMMITTED"
    DISCARDED = "DISCARDED"
    PENDING = "PENDING"

    def __str__(self) -> str:
        return str(self.value)
