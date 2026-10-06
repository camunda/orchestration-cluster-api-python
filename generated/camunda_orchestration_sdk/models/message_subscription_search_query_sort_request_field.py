from enum import StrEnum


class MessageSubscriptionSearchQuerySortRequestField(StrEnum):
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
