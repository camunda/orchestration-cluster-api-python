from enum import Enum


class AdvancedClusterVariableKindFilterEq(str, Enum):
    JSON = "JSON"
    SECRET_REFERENCE = "SECRET_REFERENCE"

    def __str__(self) -> str:
        return str(self.value)
