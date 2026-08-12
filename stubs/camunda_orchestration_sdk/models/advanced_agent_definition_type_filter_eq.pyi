from enum import Enum

class AdvancedAgentDefinitionTypeFilterEq(str, Enum):
    AI_AGENT_SUB_PROCESS = "AI_AGENT_SUB_PROCESS"
    AI_AGENT_TASK = "AI_AGENT_TASK"
    EXTERNAL_AGENT = "EXTERNAL_AGENT"
    def __str__(self) -> str: ...
