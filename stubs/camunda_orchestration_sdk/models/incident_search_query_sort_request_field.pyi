from enum import StrEnum
class IncidentSearchQuerySortRequestField(StrEnum):
    CREATIONTIME = "creationTime"
    ELEMENTID = "elementId"
    ELEMENTINSTANCEKEY = "elementInstanceKey"
    ERRORTYPE = "errorType"
    INCIDENTKEY = "incidentKey"
    JOBKEY = "jobKey"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    PROCESSINSTANCEKEY = "processInstanceKey"
    STATE = "state"
    TENANTID = "tenantId"
    def __str__(self) -> str: ...
