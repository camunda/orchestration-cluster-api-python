from enum import Enum

class AgentInstanceHistoryCommitStatusExactMatch(str, Enum):
    COMMITTED = "COMMITTED"
    DISCARDED = "DISCARDED"
    PENDING = "PENDING"
    def __str__(self) -> str: ...
