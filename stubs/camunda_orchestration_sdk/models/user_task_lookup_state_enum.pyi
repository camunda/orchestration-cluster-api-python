from enum import Enum

class UserTaskLookupStateEnum(str, Enum):
    ASSIGNING = "ASSIGNING"
    CANCELING = "CANCELING"
    COMPLETING = "COMPLETING"
    CREATED = "CREATED"
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    def __str__(self) -> str: ...
