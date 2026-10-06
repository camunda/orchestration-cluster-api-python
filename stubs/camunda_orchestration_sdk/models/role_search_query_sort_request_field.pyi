from enum import StrEnum
class RoleSearchQuerySortRequestField(StrEnum):
    NAME = "name"
    ROLEID = "roleId"
    def __str__(self) -> str: ...
