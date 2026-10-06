from enum import StrEnum
class BatchOperationItemSearchQuerySortRequestField(StrEnum):
    BATCHOPERATIONKEY = "batchOperationKey"
    ITEMKEY = "itemKey"
    PROCESSEDDATE = "processedDate"
    PROCESSINSTANCEKEY = "processInstanceKey"
    STATE = "state"
    def __str__(self) -> str: ...
