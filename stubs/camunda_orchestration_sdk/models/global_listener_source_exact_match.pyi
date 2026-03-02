from enum import Enum
class GlobalListenerSourceExactMatch(str, Enum):
    API = "API"
    CONFIGURATION = "CONFIGURATION"
    def __str__(self) -> str: ...
