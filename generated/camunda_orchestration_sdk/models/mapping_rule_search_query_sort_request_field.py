from enum import StrEnum


class MappingRuleSearchQuerySortRequestField(StrEnum):
    CLAIMNAME = "claimName"
    CLAIMVALUE = "claimValue"
    MAPPINGRULEID = "mappingRuleId"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
