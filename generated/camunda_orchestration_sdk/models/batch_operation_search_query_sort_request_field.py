from enum import StrEnum


class BatchOperationSearchQuerySortRequestField(StrEnum):
    ACTORID = "actorId"
    ACTORTYPE = "actorType"
    BATCHOPERATIONKEY = "batchOperationKey"
    ENDDATE = "endDate"
    OPERATIONTYPE = "operationType"
    STARTDATE = "startDate"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
