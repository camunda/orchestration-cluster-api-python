from enum import StrEnum
class OwnerTypeEnum(StrEnum):
    CLIENT = "CLIENT"
    GROUP = "GROUP"
    MAPPING_RULE = "MAPPING_RULE"
    ROLE = "ROLE"
    UNSPECIFIED = "UNSPECIFIED"
    USER = "USER"
    def __str__(self) -> str: ...
