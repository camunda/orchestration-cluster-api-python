from enum import Enum


class ElementInstanceWaitStateQuerySortRequestField(str, Enum):
    ELEMENTID = "elementId"
    ELEMENTINSTANCEKEY = "elementInstanceKey"
    PROCESSINSTANCEKEY = "processInstanceKey"
    ROOTPROCESSINSTANCEKEY = "rootProcessInstanceKey"

    def __str__(self) -> str:
        return str(self.value)
