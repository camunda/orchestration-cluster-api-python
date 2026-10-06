from enum import StrEnum
class AdvancedJobKindFilterNeq(StrEnum):
    AD_HOC_SUB_PROCESS = "AD_HOC_SUB_PROCESS"
    BPMN_ELEMENT = "BPMN_ELEMENT"
    EXECUTION_LISTENER = "EXECUTION_LISTENER"
    TASK_LISTENER = "TASK_LISTENER"
    def __str__(self) -> str: ...
