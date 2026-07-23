from enum import Enum

class AdvancedClusterVariableKindFilterNeq(str, Enum):
    JSON = "JSON"
    SECRET_REFERENCE = "SECRET_REFERENCE"
    def __str__(self) -> str: ...
