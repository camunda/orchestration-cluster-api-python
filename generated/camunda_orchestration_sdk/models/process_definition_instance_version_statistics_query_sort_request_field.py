from enum import StrEnum


class ProcessDefinitionInstanceVersionStatisticsQuerySortRequestField(StrEnum):
    ACTIVEINSTANCESWITHINCIDENTCOUNT = "activeInstancesWithIncidentCount"
    ACTIVEINSTANCESWITHOUTINCIDENTCOUNT = "activeInstancesWithoutIncidentCount"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    PROCESSDEFINITIONNAME = "processDefinitionName"
    PROCESSDEFINITIONVERSION = "processDefinitionVersion"

    def __str__(self) -> str:
        return str(self.value)
