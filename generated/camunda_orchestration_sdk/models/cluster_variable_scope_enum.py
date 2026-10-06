from enum import StrEnum


class ClusterVariableScopeEnum(StrEnum):
    GLOBAL = "GLOBAL"
    TENANT = "TENANT"

    def __str__(self) -> str:
        return str(self.value)
