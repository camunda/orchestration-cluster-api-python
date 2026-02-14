from enum import Enum


class PartitionHealth(str, Enum):
    DEAD = "dead"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

    def __str__(self) -> str:
        return str(self.value)
