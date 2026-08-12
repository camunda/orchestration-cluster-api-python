from enum import Enum


class AgentInstanceHistoryItemResultRole(str, Enum):
    ASSISTANT = "ASSISTANT"
    CONFIGURATION = "CONFIGURATION"
    TOOL_RESULT = "TOOL_RESULT"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)
