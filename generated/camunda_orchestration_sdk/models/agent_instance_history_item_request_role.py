from enum import Enum


class AgentInstanceHistoryItemRequestRole(str, Enum):
    ASSISTANT = "ASSISTANT"
    TOOL_RESULT = "TOOL_RESULT"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)
