from enum import Enum

class AgentInstanceHistorySearchQuerySortRequestField(str, Enum):
    HISTORYITEMKEY = "historyItemKey"
    ITERATION = "iteration"
    PRODUCEDAT = "producedAt"
    def __str__(self) -> str: ...
