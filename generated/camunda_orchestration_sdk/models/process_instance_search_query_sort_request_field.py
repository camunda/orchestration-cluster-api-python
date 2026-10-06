from enum import StrEnum


class ProcessInstanceSearchQuerySortRequestField(StrEnum):
    BUSINESSID = "businessId"
    ENDDATE = "endDate"
    HASINCIDENT = "hasIncident"
    PARENTELEMENTINSTANCEKEY = "parentElementInstanceKey"
    PARENTPROCESSINSTANCEKEY = "parentProcessInstanceKey"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    PROCESSDEFINITIONNAME = "processDefinitionName"
    PROCESSDEFINITIONVERSION = "processDefinitionVersion"
    PROCESSDEFINITIONVERSIONTAG = "processDefinitionVersionTag"
    PROCESSINSTANCEKEY = "processInstanceKey"
    STARTDATE = "startDate"
    STATE = "state"
    TENANTID = "tenantId"

    def __str__(self) -> str:
        return str(self.value)
