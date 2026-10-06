from enum import StrEnum
class CategoryExactMatch(StrEnum):
    ADMIN = "ADMIN"
    DEPLOYED_RESOURCES = "DEPLOYED_RESOURCES"
    USER_TASKS = "USER_TASKS"
    def __str__(self) -> str: ...
