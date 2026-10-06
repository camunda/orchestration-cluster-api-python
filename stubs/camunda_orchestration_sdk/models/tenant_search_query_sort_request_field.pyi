from enum import StrEnum
class TenantSearchQuerySortRequestField(StrEnum):
    KEY = "key"
    NAME = "name"
    TENANTID = "tenantId"
    def __str__(self) -> str: ...
