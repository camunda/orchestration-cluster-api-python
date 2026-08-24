from enum import Enum

class ClusterBalanceResponseState(str, Enum):
    BALANCED = "BALANCED"
    BALANCING = "BALANCING"
    UNBALANCED = "UNBALANCED"
    def __str__(self) -> str: ...
