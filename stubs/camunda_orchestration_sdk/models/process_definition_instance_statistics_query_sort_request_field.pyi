from enum import StrEnum
class ProcessDefinitionInstanceStatisticsQuerySortRequestField(StrEnum):
    ACTIVEINSTANCESWITHINCIDENTCOUNT = "activeInstancesWithIncidentCount"
    ACTIVEINSTANCESWITHOUTINCIDENTCOUNT = "activeInstancesWithoutIncidentCount"
    PROCESSDEFINITIONID = "processDefinitionId"
    def __str__(self) -> str: ...
