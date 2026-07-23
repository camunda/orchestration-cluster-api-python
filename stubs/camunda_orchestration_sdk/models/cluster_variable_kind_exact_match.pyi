from enum import Enum

class ClusterVariableKindExactMatch(str, Enum):
    JSON = "JSON"
    SECRET_REFERENCE = "SECRET_REFERENCE"
    def __str__(self) -> str: ...
