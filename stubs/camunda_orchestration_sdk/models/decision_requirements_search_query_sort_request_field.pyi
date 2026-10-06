from enum import StrEnum
class DecisionRequirementsSearchQuerySortRequestField(StrEnum):
    DECISIONREQUIREMENTSID = "decisionRequirementsId"
    DECISIONREQUIREMENTSKEY = "decisionRequirementsKey"
    DECISIONREQUIREMENTSNAME = "decisionRequirementsName"
    TENANTID = "tenantId"
    VERSION = "version"
    def __str__(self) -> str: ...
