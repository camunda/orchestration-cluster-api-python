from enum import Enum

class ClusterRebalanceOperationPartitionProgress(str, Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    TRANSFERRING = "TRANSFERRING"
    def __str__(self) -> str: ...
