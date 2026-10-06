from enum import StrEnum
class UserTaskSearchQuerySortRequestField(StrEnum):
    COMPLETIONDATE = "completionDate"
    CREATIONDATE = "creationDate"
    DUEDATE = "dueDate"
    FOLLOWUPDATE = "followUpDate"
    NAME = "name"
    PRIORITY = "priority"
    def __str__(self) -> str: ...
