from enum import Enum

class MappingRuleSearchQuerySortRequestField(str, Enum):
    CLAIMNAME = "claimName"
    CLAIMVALUE = "claimValue"
    MAPPINGRULEID = "mappingRuleId"
    NAME = "name"
    def __str__(self) -> str: ...
