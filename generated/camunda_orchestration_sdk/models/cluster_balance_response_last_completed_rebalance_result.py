from enum import Enum


class ClusterBalanceResponseLastCompletedRebalanceResult(str, Enum):
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    def __str__(self) -> str:
        return str(self.value)
