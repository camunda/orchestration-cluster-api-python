from enum import Enum
class GlobalListenerSourceEnum(str, Enum):
    API = "API"
    CONFIGURATION = "CONFIGURATION"
    def __str__(self) -> str: ...
