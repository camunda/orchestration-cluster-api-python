from enum import Enum


class AdvancedJobListenerEventTypeFilterEq(str, Enum):
    ASSIGNING = "ASSIGNING"
    BEFORE_ALL = "BEFORE_ALL"
    CANCEL = "CANCEL"
    CANCELING = "CANCELING"
    COMPLETING = "COMPLETING"
    CREATING = "CREATING"
    END = "END"
    START = "START"
    UNSPECIFIED = "UNSPECIFIED"
    UPDATING = "UPDATING"

    def __str__(self) -> str:
        return str(self.value)
