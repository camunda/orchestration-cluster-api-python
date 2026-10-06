from enum import StrEnum


class GlobalTaskListenerSearchQuerySortRequestField(StrEnum):
    AFTERNONGLOBAL = "afterNonGlobal"
    ID = "id"
    PRIORITY = "priority"
    SOURCE = "source"
    TYPE = "type"

    def __str__(self) -> str:
        return str(self.value)
