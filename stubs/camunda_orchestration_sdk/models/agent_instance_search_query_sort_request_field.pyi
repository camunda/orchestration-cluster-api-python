from enum import Enum

class AgentInstanceSearchQuerySortRequestField(str, Enum):
    AGENTINSTANCEKEY = "agentInstanceKey"
    COMPLETIONDATE = "completionDate"
    CREATIONDATE = "creationDate"
    ELEMENTID = "elementId"
    LASTUPDATEDDATE = "lastUpdatedDate"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    PROCESSINSTANCEKEY = "processInstanceKey"
    ROOTPROCESSINSTANCEKEY = "rootProcessInstanceKey"
    STATUS = "status"
    TENANTID = "tenantId"
    def __str__(self) -> str: ...
