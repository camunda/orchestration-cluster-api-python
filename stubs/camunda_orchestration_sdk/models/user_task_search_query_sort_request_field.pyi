from enum import Enum

class UserTaskSearchQuerySortRequestField(str, Enum):
    BUSINESSID = "businessId"
    COMPLETIONDATE = "completionDate"
    CREATIONDATE = "creationDate"
    DUEDATE = "dueDate"
    FOLLOWUPDATE = "followUpDate"
    NAME = "name"
    PRIORITY = "priority"
    def __str__(self) -> str: ...
