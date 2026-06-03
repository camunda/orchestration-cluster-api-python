from enum import Enum
class AdvancedDecisionInstanceStateFilterNeq(str, Enum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    UNSPECIFIED = "UNSPECIFIED"
    def __str__(self) -> str: ...
