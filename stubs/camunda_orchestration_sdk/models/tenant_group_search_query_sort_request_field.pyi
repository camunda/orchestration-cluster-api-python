from enum import Enum

class TenantGroupSearchQuerySortRequestField(str, Enum):
    GROUPID = "groupId"
    def __str__(self) -> str: ...
