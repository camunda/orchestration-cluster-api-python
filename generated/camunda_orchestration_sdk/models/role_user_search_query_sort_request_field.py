from enum import StrEnum


class RoleUserSearchQuerySortRequestField(StrEnum):
    USERNAME = "username"

    def __str__(self) -> str:
        return str(self.value)
