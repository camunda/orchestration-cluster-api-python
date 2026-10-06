from enum import StrEnum
class ClusterVariableSearchQuerySortRequestField(StrEnum):
    NAME = "name"
    SCOPE = "scope"
    TENANTID = "tenantId"
    VALUE = "value"
    def __str__(self) -> str: ...
