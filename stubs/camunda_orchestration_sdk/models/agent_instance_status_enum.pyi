from enum import Enum

class AgentInstanceStatusEnum(str, Enum):
    COMPLETED = "COMPLETED"
    IDLE = "IDLE"
    INITIALIZING = "INITIALIZING"
    THINKING = "THINKING"
    TOOL_CALLING = "TOOL_CALLING"
    TOOL_DISCOVERY = "TOOL_DISCOVERY"
    def __str__(self) -> str: ...
