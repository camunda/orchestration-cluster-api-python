from enum import Enum

class ClusterVariableSearchQuerySortRequestField(str, Enum):
    NAME = "name"
    SCOPE = "scope"
    TENANTID = "tenantId"
    VALUE = "value"
    def __str__(self) -> str: ...
