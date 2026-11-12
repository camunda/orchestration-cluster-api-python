from enum import Enum


class RoleClientSearchQuerySortRequestField(str, Enum):
    CLIENTID = "clientId"

    def __str__(self) -> str:
        return str(self.value)
