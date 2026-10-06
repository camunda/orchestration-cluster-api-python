from enum import StrEnum


class TenantUserSearchQuerySortRequestField(StrEnum):
    USERNAME = "username"

    def __str__(self) -> str:
        return str(self.value)
