from enum import Enum


class AgentInstanceMessageContentTypeEnum(str, Enum):
    DOCUMENT = "DOCUMENT"
    OBJECT = "OBJECT"
    TEXT = "TEXT"

    def __str__(self) -> str:
        return str(self.value)
