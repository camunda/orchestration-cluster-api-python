from enum import Enum

class MessageSubscriptionTypeEnum(str, Enum):
    PROCESS_EVENT = "PROCESS_EVENT"
    START_EVENT = "START_EVENT"
    def __str__(self) -> str: ...
