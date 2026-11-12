from enum import Enum


class IncidentProcessInstanceStatisticsByDefinitionQuerySortRequestField(str, Enum):
    ACTIVEINSTANCESWITHERRORCOUNT = "activeInstancesWithErrorCount"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    TENANTID = "tenantId"

    def __str__(self) -> str:
        return str(self.value)
