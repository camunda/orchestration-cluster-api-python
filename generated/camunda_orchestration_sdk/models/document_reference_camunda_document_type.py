from enum import StrEnum


class DocumentReferenceCamundaDocumentType(StrEnum):
    CAMUNDA = "camunda"

    def __str__(self) -> str:
        return str(self.value)
