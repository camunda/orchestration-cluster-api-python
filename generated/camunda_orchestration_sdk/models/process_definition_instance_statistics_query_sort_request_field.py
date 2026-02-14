from enum import Enum


class ProcessDefinitionInstanceStatisticsQuerySortRequestField(str, Enum):
    ACTIVEINSTANCESWITHINCIDENTCOUNT = "activeInstancesWithIncidentCount"
    ACTIVEINSTANCESWITHOUTINCIDENTCOUNT = "activeInstancesWithoutIncidentCount"
    PROCESSDEFINITIONID = "processDefinitionId"

    def __str__(self) -> str:
        return str(self.value)
