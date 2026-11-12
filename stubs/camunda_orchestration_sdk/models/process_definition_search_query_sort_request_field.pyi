from enum import Enum
class ProcessDefinitionSearchQuerySortRequestField(str, Enum):
    NAME = "name"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    RESOURCENAME = "resourceName"
    TENANTID = "tenantId"
    VERSION = "version"
    VERSIONTAG = "versionTag"
    def __str__(self) -> str: ...
