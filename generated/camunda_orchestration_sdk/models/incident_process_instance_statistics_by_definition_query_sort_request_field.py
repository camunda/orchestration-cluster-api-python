from enum import StrEnum


class IncidentProcessInstanceStatisticsByDefinitionQuerySortRequestField(StrEnum):
    ACTIVEINSTANCESWITHERRORCOUNT = "activeInstancesWithErrorCount"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    TENANTID = "tenantId"

    def __str__(self) -> str:
        return str(self.value)
