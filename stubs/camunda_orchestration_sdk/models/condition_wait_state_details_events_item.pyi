from enum import Enum

class ConditionWaitStateDetailsEventsItem(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    def __str__(self) -> str: ...
