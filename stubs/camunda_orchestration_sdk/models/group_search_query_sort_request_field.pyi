from enum import Enum
class GroupSearchQuerySortRequestField(str, Enum):
    GROUPID = "groupId"
    NAME = "name"
    def __str__(self) -> str: ...
