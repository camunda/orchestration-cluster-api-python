from enum import Enum

class JobListenerEventTypeEnum(str, Enum):
    ASSIGNING = "ASSIGNING"
    CANCELING = "CANCELING"
    COMPLETING = "COMPLETING"
    CREATING = "CREATING"
    END = "END"
    START = "START"
    UNSPECIFIED = "UNSPECIFIED"
    UPDATING = "UPDATING"
    def __str__(self) -> str: ...
