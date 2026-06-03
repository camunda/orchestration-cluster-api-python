from enum import Enum
class ClusterVariableScopeExactMatch(str, Enum):
    GLOBAL = "GLOBAL"
    TENANT = "TENANT"
    def __str__(self) -> str: ...
