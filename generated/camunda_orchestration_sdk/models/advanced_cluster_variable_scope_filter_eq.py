from enum import StrEnum


class AdvancedClusterVariableScopeFilterEq(StrEnum):
    GLOBAL = "GLOBAL"
    TENANT = "TENANT"

    def __str__(self) -> str:
        return str(self.value)
