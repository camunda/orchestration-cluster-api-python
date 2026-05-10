from enum import Enum

class AuthorizationSearchQuerySortRequestField(str, Enum):
    OWNERID = "ownerId"
    OWNERTYPE = "ownerType"
    RESOURCEID = "resourceId"
    RESOURCEPROPERTYNAME = "resourcePropertyName"
    RESOURCETYPE = "resourceType"
    def __str__(self) -> str: ...
