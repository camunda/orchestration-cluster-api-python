from enum import Enum


class DocumentReferenceCamundaDocumentType(str, Enum):
    CAMUNDA = "camunda"

    def __str__(self) -> str:
        return str(self.value)
