from enum import StrEnum


class PartitionHealth(StrEnum):
    DEAD = "dead"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

    def __str__(self) -> str:
        return str(self.value)
