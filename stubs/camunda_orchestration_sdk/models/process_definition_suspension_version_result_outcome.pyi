from enum import Enum

class ProcessDefinitionSuspensionVersionResultOutcome(str, Enum):
    ALREADY_SUSPENDED = "ALREADY_SUSPENDED"
    DRAINING = "DRAINING"
    SUSPENDED = "SUSPENDED"
    def __str__(self) -> str: ...
