from enum import Enum
class AdvancedMessageSubscriptionStateFilterEq(str, Enum):
    CORRELATED = "CORRELATED"
    CREATED = "CREATED"
    DELETED = "DELETED"
    MIGRATED = "MIGRATED"
    def __str__(self) -> str: ...
