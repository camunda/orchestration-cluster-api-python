from enum import StrEnum


class GlobalTaskListenerEventTypeExactMatch(StrEnum):
    ALL = "all"
    ASSIGNING = "assigning"
    CANCELING = "canceling"
    COMPLETING = "completing"
    CREATING = "creating"
    UPDATING = "updating"

    def __str__(self) -> str:
        return str(self.value)
