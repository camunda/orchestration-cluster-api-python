from enum import Enum


class UserSearchQuerySortRequestField(str, Enum):
    EMAIL = "email"
    NAME = "name"
    USERNAME = "username"

    def __str__(self) -> str:
        return str(self.value)
