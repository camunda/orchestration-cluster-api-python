from enum import StrEnum


class GroupClientSearchQuerySortRequestField(StrEnum):
    CLIENTID = "clientId"

    def __str__(self) -> str:
        return str(self.value)
