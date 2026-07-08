from enum import Enum

class ChangeClusterModeMode(str, Enum):
    PROCESSING = "PROCESSING"
    RECOVERING = "RECOVERING"
    def __str__(self) -> str: ...
