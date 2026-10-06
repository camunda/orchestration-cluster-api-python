from enum import StrEnum
class IncidentProcessInstanceStatisticsByErrorQuerySortRequestField(StrEnum):
    ACTIVEINSTANCESWITHERRORCOUNT = "activeInstancesWithErrorCount"
    ERRORMESSAGE = "errorMessage"
    def __str__(self) -> str: ...
