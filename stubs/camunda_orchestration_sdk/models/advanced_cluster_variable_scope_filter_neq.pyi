from enum import StrEnum
class AdvancedClusterVariableScopeFilterNeq(StrEnum):
    GLOBAL = "GLOBAL"
    TENANT = "TENANT"
    def __str__(self) -> str: ...
