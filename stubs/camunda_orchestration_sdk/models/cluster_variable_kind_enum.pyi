from enum import Enum

class ClusterVariableKindEnum(str, Enum):
    JSON = "JSON"
    SECRET_REFERENCE = "SECRET_REFERENCE"
    def __str__(self) -> str: ...
