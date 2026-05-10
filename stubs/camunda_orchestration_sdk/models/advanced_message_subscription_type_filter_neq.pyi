from enum import Enum

class AdvancedMessageSubscriptionTypeFilterNeq(str, Enum):
    PROCESS_EVENT = "PROCESS_EVENT"
    START_EVENT = "START_EVENT"
    def __str__(self) -> str: ...
