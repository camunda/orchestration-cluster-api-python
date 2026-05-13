from enum import Enum


class CloudStage(str, Enum):
    DEV = "dev"
    INT = "int"
    PROD = "prod"

    def __str__(self) -> str:
        return str(self.value)
