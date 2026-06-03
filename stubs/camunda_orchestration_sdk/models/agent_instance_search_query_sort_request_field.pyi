from enum import Enum
class AgentInstanceSearchQuerySortRequestField(str, Enum):
    COMPLETIONDATE = "completionDate"
    CREATIONDATE = "creationDate"
    LASTUPDATEDDATE = "lastUpdatedDate"
    STATUS = "status"
    def __str__(self) -> str: ...
