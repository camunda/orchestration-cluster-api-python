from enum import Enum
class AgentInstanceUpdateStatusEnum(str, Enum):
    IDLE = "IDLE"
    THINKING = "THINKING"
    TOOL_CALLING = "TOOL_CALLING"
    TOOL_DISCOVERY = "TOOL_DISCOVERY"
    def __str__(self) -> str: ...
