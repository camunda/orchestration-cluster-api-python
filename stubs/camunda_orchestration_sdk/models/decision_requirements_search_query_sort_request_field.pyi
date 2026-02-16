from enum import Enum
class DecisionRequirementsSearchQuerySortRequestField(str, Enum):
    DECISIONREQUIREMENTSID = "decisionRequirementsId"
    DECISIONREQUIREMENTSKEY = "decisionRequirementsKey"
    DECISIONREQUIREMENTSNAME = "decisionRequirementsName"
    TENANTID = "tenantId"
    VERSION = "version"
    def __str__(self) -> str: ...
