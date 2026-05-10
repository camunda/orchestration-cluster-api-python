from enum import Enum

class ElementInstanceSearchQuerySortRequestField(str, Enum):
    ELEMENTID = "elementId"
    ELEMENTINSTANCEKEY = "elementInstanceKey"
    ELEMENTNAME = "elementName"
    ENDDATE = "endDate"
    INCIDENTKEY = "incidentKey"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    PROCESSINSTANCEKEY = "processInstanceKey"
    STARTDATE = "startDate"
    STATE = "state"
    TENANTID = "tenantId"
    TYPE = "type"
    def __str__(self) -> str: ...
