from enum import Enum
class UserTaskVariableSearchQuerySortRequestField(str, Enum):
    NAME = "name"
    PROCESSINSTANCEKEY = "processInstanceKey"
    SCOPEKEY = "scopeKey"
    TENANTID = "tenantId"
    VALUE = "value"
    VARIABLEKEY = "variableKey"
    def __str__(self) -> str: ...
