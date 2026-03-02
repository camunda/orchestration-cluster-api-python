from enum import Enum
class GlobalTaskListenerEventTypeExactMatch(str, Enum):
    ALL = "all"
    ASSIGNING = "assigning"
    CANCELING = "canceling"
    COMPLETING = "completing"
    CREATING = "creating"
    UPDATING = "updating"
    def __str__(self) -> str: ...
