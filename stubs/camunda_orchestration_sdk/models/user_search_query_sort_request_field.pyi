from enum import StrEnum
class UserSearchQuerySortRequestField(StrEnum):
    EMAIL = "email"
    NAME = "name"
    USERNAME = "username"
    def __str__(self) -> str: ...
