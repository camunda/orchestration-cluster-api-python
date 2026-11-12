from enum import Enum


class MessageSubscriptionSearchQuerySortRequestField(str, Enum):
    CORRELATIONKEY = "correlationKey"
    ELEMENTID = "elementId"
    ELEMENTINSTANCEKEY = "elementInstanceKey"
    LASTUPDATEDDATE = "lastUpdatedDate"
    MESSAGENAME = "messageName"
    MESSAGESUBSCRIPTIONKEY = "messageSubscriptionKey"
    MESSAGESUBSCRIPTIONSTATE = "messageSubscriptionState"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSINSTANCEKEY = "processInstanceKey"
    TENANTID = "tenantId"

    def __str__(self) -> str:
        return str(self.value)
