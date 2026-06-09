from enum import Enum

class AdvancedAgentInstanceHistoryRoleFilterNeq(str, Enum):
    ASSISTANT = "ASSISTANT"
    TOOL_RESULT = "TOOL_RESULT"
    USER = "USER"
    def __str__(self) -> str: ...
