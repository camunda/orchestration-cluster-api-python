from enum import Enum

class AdvancedDecisionInstanceStateFilterNeq(str, Enum):
    EVALUATED = "EVALUATED"
    FAILED = "FAILED"
    UNSPECIFIED = "UNSPECIFIED"
    def __str__(self) -> str: ...
