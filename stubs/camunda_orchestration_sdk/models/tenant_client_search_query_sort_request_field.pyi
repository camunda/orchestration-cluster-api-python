from enum import Enum

class TenantClientSearchQuerySortRequestField(str, Enum):
    CLIENTID = "clientId"
    def __str__(self) -> str: ...
