from enum import StrEnum
class UserTaskStateExactMatch(StrEnum):
    ASSIGNING = "ASSIGNING"
    CANCELED = "CANCELED"
    CANCELING = "CANCELING"
    COMPLETED = "COMPLETED"
    COMPLETING = "COMPLETING"
    CREATED = "CREATED"
    CREATING = "CREATING"
    FAILED = "FAILED"
    UPDATING = "UPDATING"
    def __str__(self) -> str: ...
