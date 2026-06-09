from enum import Enum

class AdvancedAgentInstanceHistoryCommitStatusFilterNeq(str, Enum):
    COMMITTED = "COMMITTED"
    DISCARDED = "DISCARDED"
    PENDING = "PENDING"
    def __str__(self) -> str: ...
