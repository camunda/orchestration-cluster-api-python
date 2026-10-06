from enum import StrEnum


class ClusterVariableScopeExactMatch(StrEnum):
    GLOBAL = "GLOBAL"
    TENANT = "TENANT"

    def __str__(self) -> str:
        return str(self.value)
