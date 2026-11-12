from enum import Enum


class CorrelatedMessageSubscriptionSearchQuerySortRequestField(str, Enum):
    CORRELATIONKEY = "correlationKey"
    CORRELATIONTIME = "correlationTime"
    ELEMENTID = "elementId"
    ELEMENTINSTANCEKEY = "elementInstanceKey"
    MESSAGEKEY = "messageKey"
    MESSAGENAME = "messageName"
    PARTITIONID = "partitionId"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    PROCESSINSTANCEKEY = "processInstanceKey"
    SUBSCRIPTIONKEY = "subscriptionKey"
    TENANTID = "tenantId"

    def __str__(self) -> str:
        return str(self.value)
