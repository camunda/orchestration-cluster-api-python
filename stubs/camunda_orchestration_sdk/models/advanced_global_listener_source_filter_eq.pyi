from enum import Enum
class AdvancedGlobalListenerSourceFilterEq(str, Enum):
    API = "API"
    CONFIGURATION = "CONFIGURATION"
    def __str__(self) -> str: ...
