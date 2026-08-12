from enum import Enum


class AgentDefinitionSearchQuerySortRequestField(str, Enum):
    AGENTDEFINITIONKEY = "agentDefinitionKey"
    AGENTTYPE = "agentType"
    ELEMENTID = "elementId"
    NAME = "name"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    PROCESSDEFINITIONVERSION = "processDefinitionVersion"
    PROCESSDEFINITIONVERSIONTAG = "processDefinitionVersionTag"
    TENANTID = "tenantId"

    def __str__(self) -> str:
        return str(self.value)
