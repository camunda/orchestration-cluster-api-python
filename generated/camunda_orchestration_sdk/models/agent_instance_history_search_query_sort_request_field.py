from enum import Enum


class AgentInstanceHistorySearchQuerySortRequestField(str, Enum):
    HISTORYITEMKEY = "historyItemKey"
    LOOPITERATION = "loopIteration"
    PRODUCEDAT = "producedAt"

    def __str__(self) -> str:
        return str(self.value)
