from enum import Enum

class ClusterStatusResponseStatus(str, Enum):
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    HEALTHY = "HEALTHY"
    def __str__(self) -> str: ...
