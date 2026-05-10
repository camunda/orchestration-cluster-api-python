from enum import Enum

class MessageSubscriptionSearchQuerySortRequestField(str, Enum):
    CORRELATIONKEY = "correlationKey"
    ELEMENTID = "elementId"
    ELEMENTINSTANCEKEY = "elementInstanceKey"
    INBOUNDCONNECTORTYPE = "inboundConnectorType"
    LASTUPDATEDDATE = "lastUpdatedDate"
    MESSAGENAME = "messageName"
    MESSAGESUBSCRIPTIONKEY = "messageSubscriptionKey"
    MESSAGESUBSCRIPTIONSTATE = "messageSubscriptionState"
    MESSAGESUBSCRIPTIONTYPE = "messageSubscriptionType"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONNAME = "processDefinitionName"
    PROCESSDEFINITIONVERSION = "processDefinitionVersion"
    PROCESSINSTANCEKEY = "processInstanceKey"
    TENANTID = "tenantId"
    TOOLNAME = "toolName"
    def __str__(self) -> str: ...
