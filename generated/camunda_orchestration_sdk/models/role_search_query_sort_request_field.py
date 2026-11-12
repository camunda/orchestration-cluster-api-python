from enum import Enum


class RoleSearchQuerySortRequestField(str, Enum):
    NAME = "name"
    ROLEID = "roleId"

    def __str__(self) -> str:
        return str(self.value)
