from enum import StrEnum
class MessageSubscriptionStateExactMatch(StrEnum):
    CORRELATED = "CORRELATED"
    CREATED = "CREATED"
    DELETED = "DELETED"
    MIGRATED = "MIGRATED"
    def __str__(self) -> str: ...
