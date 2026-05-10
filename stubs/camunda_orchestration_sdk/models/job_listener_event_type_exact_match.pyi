from enum import Enum

class JobListenerEventTypeExactMatch(str, Enum):
    ASSIGNING = "ASSIGNING"
    BEFORE_ALL = "BEFORE_ALL"
    CANCELING = "CANCELING"
    COMPLETING = "COMPLETING"
    CREATING = "CREATING"
    END = "END"
    START = "START"
    UNSPECIFIED = "UNSPECIFIED"
    UPDATING = "UPDATING"
    def __str__(self) -> str: ...
