from enum import StrEnum


class AuthorizationSearchQuerySortRequestField(StrEnum):
    OWNERID = "ownerId"
    OWNERTYPE = "ownerType"
    RESOURCEID = "resourceId"
    RESOURCEPROPERTYNAME = "resourcePropertyName"
    RESOURCETYPE = "resourceType"

    def __str__(self) -> str:
        return str(self.value)
