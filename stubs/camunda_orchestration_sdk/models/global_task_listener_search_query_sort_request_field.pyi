from enum import Enum
class GlobalTaskListenerSearchQuerySortRequestField(str, Enum):
    AFTERNONGLOBAL = "afterNonGlobal"
    ID = "id"
    PRIORITY = "priority"
    SOURCE = "source"
    TYPE = "type"
    def __str__(self) -> str: ...
