from enum import Enum

class ProcessDefinitionResumptionVersionResultOutcome(str, Enum):
    ALREADY_RESUMED = "ALREADY_RESUMED"
    DRAINING = "DRAINING"
    RESUMED = "RESUMED"
    def __str__(self) -> str: ...
