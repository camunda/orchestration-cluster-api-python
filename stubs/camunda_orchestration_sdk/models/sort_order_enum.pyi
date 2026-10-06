from enum import StrEnum
class SortOrderEnum(StrEnum):
    ASC = "ASC"
    DESC = "DESC"
    def __str__(self) -> str: ...
