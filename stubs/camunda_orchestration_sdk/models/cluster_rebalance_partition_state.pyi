from enum import Enum

class ClusterRebalancePartitionState(str, Enum):
    BALANCED = "BALANCED"
    TRANSFERRING = "TRANSFERRING"
    UNBALANCED = "UNBALANCED"
    def __str__(self) -> str: ...
