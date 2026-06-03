from enum import Enum
class IncidentProcessInstanceStatisticsByErrorQuerySortRequestField(str, Enum):
    ACTIVEINSTANCESWITHERRORCOUNT = "activeInstancesWithErrorCount"
    ERRORMESSAGE = "errorMessage"
    def __str__(self) -> str: ...
