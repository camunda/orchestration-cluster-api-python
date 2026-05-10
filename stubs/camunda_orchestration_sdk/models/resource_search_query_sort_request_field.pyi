from enum import Enum

class ResourceSearchQuerySortRequestField(str, Enum):
    DEPLOYMENTKEY = "deploymentKey"
    RESOURCEID = "resourceId"
    RESOURCEKEY = "resourceKey"
    RESOURCENAME = "resourceName"
    TENANTID = "tenantId"
    VERSION = "version"
    VERSIONTAG = "versionTag"
    def __str__(self) -> str: ...
