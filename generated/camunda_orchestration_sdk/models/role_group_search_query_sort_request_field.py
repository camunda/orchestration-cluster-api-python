from enum import Enum


class RoleGroupSearchQuerySortRequestField(str, Enum):
    GROUPID = "groupId"

    def __str__(self) -> str:
        return str(self.value)
