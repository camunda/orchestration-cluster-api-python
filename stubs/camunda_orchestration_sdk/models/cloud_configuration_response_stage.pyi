from enum import Enum

class CloudConfigurationResponseStage(str, Enum):
    DEV = "dev"
    INT = "int"
    PROD = "prod"
    def __str__(self) -> str: ...
