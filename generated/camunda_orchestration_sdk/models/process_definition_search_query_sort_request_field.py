from enum import StrEnum


class ProcessDefinitionSearchQuerySortRequestField(StrEnum):
    NAME = "name"
    PROCESSDEFINITIONID = "processDefinitionId"
    PROCESSDEFINITIONKEY = "processDefinitionKey"
    RESOURCENAME = "resourceName"
    TENANTID = "tenantId"
    VERSION = "version"
    VERSIONTAG = "versionTag"

    def __str__(self) -> str:
        return str(self.value)
