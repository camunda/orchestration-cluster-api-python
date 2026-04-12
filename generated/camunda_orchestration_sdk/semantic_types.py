from __future__ import annotations
from typing import Any, Tuple, Union
import re


class AuditLogEntityKey(str):
    def __new__(cls, value: str) -> "AuditLogEntityKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"AuditLogEntityKey must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


def lift_audit_log_entity_key(value: Any) -> AuditLogEntityKey:
    return AuditLogEntityKey(value)


def try_lift_audit_log_entity_key(
    value: Any,
) -> Tuple[bool, AuditLogEntityKey | Exception]:
    try:
        return True, lift_audit_log_entity_key(value)
    except Exception as e:
        return False, e


class AuditLogKey(str):
    def __new__(cls, value: str) -> "AuditLogKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"AuditLogKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"AuditLogKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"AuditLogKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"AuditLogKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_audit_log_key(value: Any) -> AuditLogKey:
    return AuditLogKey(value)


def try_lift_audit_log_key(value: Any) -> Tuple[bool, AuditLogKey | Exception]:
    try:
        return True, lift_audit_log_key(value)
    except Exception as e:
        return False, e


class AuthorizationKey(str):
    def __new__(cls, value: str) -> "AuthorizationKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"AuthorizationKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"AuthorizationKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"AuthorizationKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"AuthorizationKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_authorization_key(value: Any) -> AuthorizationKey:
    return AuthorizationKey(value)


def try_lift_authorization_key(value: Any) -> Tuple[bool, AuthorizationKey | Exception]:
    try:
        return True, lift_authorization_key(value)
    except Exception as e:
        return False, e


class BatchOperationKey(str):
    def __new__(cls, value: str) -> "BatchOperationKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"BatchOperationKey must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


def lift_batch_operation_key(value: Any) -> BatchOperationKey:
    return BatchOperationKey(value)


def try_lift_batch_operation_key(
    value: Any,
) -> Tuple[bool, BatchOperationKey | Exception]:
    try:
        return True, lift_batch_operation_key(value)
    except Exception as e:
        return False, e


class BusinessId(str):
    def __new__(cls, value: str) -> "BusinessId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"BusinessId must be str, got {type(value).__name__}: {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"BusinessId shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"BusinessId longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


def lift_business_id(value: Any) -> BusinessId:
    return BusinessId(value)


def try_lift_business_id(value: Any) -> Tuple[bool, BusinessId | Exception]:
    try:
        return True, lift_business_id(value)
    except Exception as e:
        return False, e


class ConditionalEvaluationKey(str):
    def __new__(cls, value: str) -> "ConditionalEvaluationKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ConditionalEvaluationKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"ConditionalEvaluationKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"ConditionalEvaluationKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"ConditionalEvaluationKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_conditional_evaluation_key(value: Any) -> ConditionalEvaluationKey:
    return ConditionalEvaluationKey(value)


def try_lift_conditional_evaluation_key(
    value: Any,
) -> Tuple[bool, ConditionalEvaluationKey | Exception]:
    try:
        return True, lift_conditional_evaluation_key(value)
    except Exception as e:
        return False, e


class DecisionDefinitionId(str):
    def __new__(cls, value: str) -> "DecisionDefinitionId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DecisionDefinitionId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[\\w_][\\w0-9_\\-\\.]*$", value) is None:
            pat = "^[\\w_][\\w0-9_\\-\\.]*$"
            raise ValueError(
                f"DecisionDefinitionId does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"DecisionDefinitionId shorter than minLength 1, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_decision_definition_id(value: Any) -> DecisionDefinitionId:
    return DecisionDefinitionId(value)


def try_lift_decision_definition_id(
    value: Any,
) -> Tuple[bool, DecisionDefinitionId | Exception]:
    try:
        return True, lift_decision_definition_id(value)
    except Exception as e:
        return False, e


class DecisionDefinitionKey(str):
    def __new__(cls, value: str) -> "DecisionDefinitionKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DecisionDefinitionKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"DecisionDefinitionKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"DecisionDefinitionKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"DecisionDefinitionKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_decision_definition_key(value: Any) -> DecisionDefinitionKey:
    return DecisionDefinitionKey(value)


def try_lift_decision_definition_key(
    value: Any,
) -> Tuple[bool, DecisionDefinitionKey | Exception]:
    try:
        return True, lift_decision_definition_key(value)
    except Exception as e:
        return False, e


class DecisionEvaluationInstanceKey(str):
    def __new__(cls, value: str) -> "DecisionEvaluationInstanceKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DecisionEvaluationInstanceKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"DecisionEvaluationInstanceKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"DecisionEvaluationInstanceKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"DecisionEvaluationInstanceKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_decision_evaluation_instance_key(value: Any) -> DecisionEvaluationInstanceKey:
    return DecisionEvaluationInstanceKey(value)


def try_lift_decision_evaluation_instance_key(
    value: Any,
) -> Tuple[bool, DecisionEvaluationInstanceKey | Exception]:
    try:
        return True, lift_decision_evaluation_instance_key(value)
    except Exception as e:
        return False, e


class DecisionEvaluationKey(str):
    def __new__(cls, value: str) -> "DecisionEvaluationKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DecisionEvaluationKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"DecisionEvaluationKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"DecisionEvaluationKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"DecisionEvaluationKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_decision_evaluation_key(value: Any) -> DecisionEvaluationKey:
    return DecisionEvaluationKey(value)


def try_lift_decision_evaluation_key(
    value: Any,
) -> Tuple[bool, DecisionEvaluationKey | Exception]:
    try:
        return True, lift_decision_evaluation_key(value)
    except Exception as e:
        return False, e


class DecisionInstanceKey(str):
    def __new__(cls, value: str) -> "DecisionInstanceKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DecisionInstanceKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"DecisionInstanceKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"DecisionInstanceKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"DecisionInstanceKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_decision_instance_key(value: Any) -> DecisionInstanceKey:
    return DecisionInstanceKey(value)


def try_lift_decision_instance_key(
    value: Any,
) -> Tuple[bool, DecisionInstanceKey | Exception]:
    try:
        return True, lift_decision_instance_key(value)
    except Exception as e:
        return False, e


class DecisionRequirementsKey(str):
    def __new__(cls, value: str) -> "DecisionRequirementsKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DecisionRequirementsKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"DecisionRequirementsKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"DecisionRequirementsKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"DecisionRequirementsKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_decision_requirements_key(value: Any) -> DecisionRequirementsKey:
    return DecisionRequirementsKey(value)


def try_lift_decision_requirements_key(
    value: Any,
) -> Tuple[bool, DecisionRequirementsKey | Exception]:
    try:
        return True, lift_decision_requirements_key(value)
    except Exception as e:
        return False, e


class DeploymentKey(str):
    def __new__(cls, value: str) -> "DeploymentKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DeploymentKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"DeploymentKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"DeploymentKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"DeploymentKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_deployment_key(value: Any) -> DeploymentKey:
    return DeploymentKey(value)


def try_lift_deployment_key(value: Any) -> Tuple[bool, DeploymentKey | Exception]:
    try:
        return True, lift_deployment_key(value)
    except Exception as e:
        return False, e


class DocumentId(str):
    def __new__(cls, value: str) -> "DocumentId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DocumentId must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


def lift_document_id(value: Any) -> DocumentId:
    return DocumentId(value)


def try_lift_document_id(value: Any) -> Tuple[bool, DocumentId | Exception]:
    try:
        return True, lift_document_id(value)
    except Exception as e:
        return False, e


class ElementId(str):
    def __new__(cls, value: str) -> "ElementId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ElementId must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


def lift_element_id(value: Any) -> ElementId:
    return ElementId(value)


def try_lift_element_id(value: Any) -> Tuple[bool, ElementId | Exception]:
    try:
        return True, lift_element_id(value)
    except Exception as e:
        return False, e


class ElementInstanceKey(str):
    def __new__(cls, value: str) -> "ElementInstanceKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ElementInstanceKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"ElementInstanceKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"ElementInstanceKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"ElementInstanceKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_element_instance_key(value: Any) -> ElementInstanceKey:
    return ElementInstanceKey(value)


def try_lift_element_instance_key(
    value: Any,
) -> Tuple[bool, ElementInstanceKey | Exception]:
    try:
        return True, lift_element_instance_key(value)
    except Exception as e:
        return False, e


class EndCursor(str):
    def __new__(cls, value: str) -> "EndCursor":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"EndCursor must be str, got {type(value).__name__}: {value!r}"
            )
        if (
            re.fullmatch(
                "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$",
                value,
            )
            is None
        ):
            pat = (
                "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$"
            )
            raise ValueError(f"EndCursor does not match pattern {pat!r}, got {value!r}")
        return super().__new__(cls, value)


def lift_end_cursor(value: Any) -> EndCursor:
    return EndCursor(value)


def try_lift_end_cursor(value: Any) -> Tuple[bool, EndCursor | Exception]:
    try:
        return True, lift_end_cursor(value)
    except Exception as e:
        return False, e


class FormId(str):
    def __new__(cls, value: str) -> "FormId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"FormId must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


def lift_form_id(value: Any) -> FormId:
    return FormId(value)


def try_lift_form_id(value: Any) -> Tuple[bool, FormId | Exception]:
    try:
        return True, lift_form_id(value)
    except Exception as e:
        return False, e


class FormKey(str):
    def __new__(cls, value: str) -> "FormKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"FormKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(f"FormKey does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"FormKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"FormKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_form_key(value: Any) -> FormKey:
    return FormKey(value)


def try_lift_form_key(value: Any) -> Tuple[bool, FormKey | Exception]:
    try:
        return True, lift_form_key(value)
    except Exception as e:
        return False, e


class GlobalListenerId(str):
    def __new__(cls, value: str) -> "GlobalListenerId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"GlobalListenerId must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


def lift_global_listener_id(value: Any) -> GlobalListenerId:
    return GlobalListenerId(value)


def try_lift_global_listener_id(
    value: Any,
) -> Tuple[bool, GlobalListenerId | Exception]:
    try:
        return True, lift_global_listener_id(value)
    except Exception as e:
        return False, e


class IncidentKey(str):
    def __new__(cls, value: str) -> "IncidentKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"IncidentKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"IncidentKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"IncidentKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"IncidentKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_incident_key(value: Any) -> IncidentKey:
    return IncidentKey(value)


def try_lift_incident_key(value: Any) -> Tuple[bool, IncidentKey | Exception]:
    try:
        return True, lift_incident_key(value)
    except Exception as e:
        return False, e


class JobKey(str):
    def __new__(cls, value: str) -> "JobKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"JobKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(f"JobKey does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"JobKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"JobKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_job_key(value: Any) -> JobKey:
    return JobKey(value)


def try_lift_job_key(value: Any) -> Tuple[bool, JobKey | Exception]:
    try:
        return True, lift_job_key(value)
    except Exception as e:
        return False, e


class MessageKey(str):
    def __new__(cls, value: str) -> "MessageKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"MessageKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"MessageKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"MessageKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"MessageKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_message_key(value: Any) -> MessageKey:
    return MessageKey(value)


def try_lift_message_key(value: Any) -> Tuple[bool, MessageKey | Exception]:
    try:
        return True, lift_message_key(value)
    except Exception as e:
        return False, e


class MessageSubscriptionKey(str):
    def __new__(cls, value: str) -> "MessageSubscriptionKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"MessageSubscriptionKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"MessageSubscriptionKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"MessageSubscriptionKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"MessageSubscriptionKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_message_subscription_key(value: Any) -> MessageSubscriptionKey:
    return MessageSubscriptionKey(value)


def try_lift_message_subscription_key(
    value: Any,
) -> Tuple[bool, MessageSubscriptionKey | Exception]:
    try:
        return True, lift_message_subscription_key(value)
    except Exception as e:
        return False, e


class ProcessDefinitionId(str):
    def __new__(cls, value: str) -> "ProcessDefinitionId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ProcessDefinitionId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[\\w_][\\w0-9_\\-\\.]*$", value) is None:
            pat = "^[\\w_][\\w0-9_\\-\\.]*$"
            raise ValueError(
                f"ProcessDefinitionId does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"ProcessDefinitionId shorter than minLength 1, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_process_definition_id(value: Any) -> ProcessDefinitionId:
    return ProcessDefinitionId(value)


def try_lift_process_definition_id(
    value: Any,
) -> Tuple[bool, ProcessDefinitionId | Exception]:
    try:
        return True, lift_process_definition_id(value)
    except Exception as e:
        return False, e


class ProcessDefinitionKey(str):
    def __new__(cls, value: str) -> "ProcessDefinitionKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ProcessDefinitionKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"ProcessDefinitionKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"ProcessDefinitionKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"ProcessDefinitionKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_process_definition_key(value: Any) -> ProcessDefinitionKey:
    return ProcessDefinitionKey(value)


def try_lift_process_definition_key(
    value: Any,
) -> Tuple[bool, ProcessDefinitionKey | Exception]:
    try:
        return True, lift_process_definition_key(value)
    except Exception as e:
        return False, e


class ProcessInstanceKey(str):
    def __new__(cls, value: str) -> "ProcessInstanceKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ProcessInstanceKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"ProcessInstanceKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"ProcessInstanceKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"ProcessInstanceKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_process_instance_key(value: Any) -> ProcessInstanceKey:
    return ProcessInstanceKey(value)


def try_lift_process_instance_key(
    value: Any,
) -> Tuple[bool, ProcessInstanceKey | Exception]:
    try:
        return True, lift_process_instance_key(value)
    except Exception as e:
        return False, e


class SignalKey(str):
    def __new__(cls, value: str) -> "SignalKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"SignalKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(f"SignalKey does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"SignalKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"SignalKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_signal_key(value: Any) -> SignalKey:
    return SignalKey(value)


def try_lift_signal_key(value: Any) -> Tuple[bool, SignalKey | Exception]:
    try:
        return True, lift_signal_key(value)
    except Exception as e:
        return False, e


class StartCursor(str):
    def __new__(cls, value: str) -> "StartCursor":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"StartCursor must be str, got {type(value).__name__}: {value!r}"
            )
        if (
            re.fullmatch(
                "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$",
                value,
            )
            is None
        ):
            pat = (
                "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$"
            )
            raise ValueError(
                f"StartCursor does not match pattern {pat!r}, got {value!r}"
            )
        return super().__new__(cls, value)


def lift_start_cursor(value: Any) -> StartCursor:
    return StartCursor(value)


def try_lift_start_cursor(value: Any) -> Tuple[bool, StartCursor | Exception]:
    try:
        return True, lift_start_cursor(value)
    except Exception as e:
        return False, e


class Tag(str):
    def __new__(cls, value: str) -> "Tag":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Tag must be str, got {type(value).__name__}: {value!r}")
        if re.fullmatch("^[A-Za-z][A-Za-z0-9_\\-:.]{0,99}$", value) is None:
            pat = "^[A-Za-z][A-Za-z0-9_\\-:.]{0,99}$"
            raise ValueError(f"Tag does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"Tag shorter than minLength 1, got {value!r}")
        if len(value) > 100:
            raise ValueError(f"Tag longer than maxLength 100, got {value!r}")
        return super().__new__(cls, value)


def lift_tag(value: Any) -> Tag:
    return Tag(value)


def try_lift_tag(value: Any) -> Tuple[bool, Tag | Exception]:
    try:
        return True, lift_tag(value)
    except Exception as e:
        return False, e


class TenantId(str):
    def __new__(cls, value: str) -> "TenantId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"TenantId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^(<default>|[A-Za-z0-9_@.+-]+)$", value) is None:
            pat = "^(<default>|[A-Za-z0-9_@.+-]+)$"
            raise ValueError(f"TenantId does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"TenantId shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"TenantId longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


def lift_tenant_id(value: Any) -> TenantId:
    return TenantId(value)


def try_lift_tenant_id(value: Any) -> Tuple[bool, TenantId | Exception]:
    try:
        return True, lift_tenant_id(value)
    except Exception as e:
        return False, e


class UserTaskKey(str):
    def __new__(cls, value: str) -> "UserTaskKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"UserTaskKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"UserTaskKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"UserTaskKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"UserTaskKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_user_task_key(value: Any) -> UserTaskKey:
    return UserTaskKey(value)


def try_lift_user_task_key(value: Any) -> Tuple[bool, UserTaskKey | Exception]:
    try:
        return True, lift_user_task_key(value)
    except Exception as e:
        return False, e


class Username(str):
    def __new__(cls, value: str) -> "Username":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"Username must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^(<default>|[A-Za-z0-9_@.+-]+)$", value) is None:
            pat = "^(<default>|[A-Za-z0-9_@.+-]+)$"
            raise ValueError(f"Username does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"Username shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"Username longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


def lift_username(value: Any) -> Username:
    return Username(value)


def try_lift_username(value: Any) -> Tuple[bool, Username | Exception]:
    try:
        return True, lift_username(value)
    except Exception as e:
        return False, e


class VariableKey(str):
    def __new__(cls, value: str) -> "VariableKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"VariableKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"VariableKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"VariableKey shorter than minLength 1, got {value!r}")
        if len(value) > 25:
            raise ValueError(f"VariableKey longer than maxLength 25, got {value!r}")
        return super().__new__(cls, value)


def lift_variable_key(value: Any) -> VariableKey:
    return VariableKey(value)


def try_lift_variable_key(value: Any) -> Tuple[bool, VariableKey | Exception]:
    try:
        return True, lift_variable_key(value)
    except Exception as e:
        return False, e


ResourceKey = Union[
    ProcessDefinitionKey, DecisionRequirementsKey, FormKey, DecisionDefinitionKey
]


def lift_resource_key(value: Any) -> ResourceKey:
    try:
        return lift_process_definition_key(value)
    except Exception:
        pass
    try:
        return lift_decision_requirements_key(value)
    except Exception:
        pass
    try:
        return lift_form_key(value)
    except Exception:
        pass
    try:
        return lift_decision_definition_key(value)
    except Exception:
        pass
    raise ValueError(
        f"ResourceKey: value {value!r} does not match any branch (ProcessDefinitionKey, DecisionRequirementsKey, FormKey, DecisionDefinitionKey)"
    )


def try_lift_resource_key(value: Any) -> Tuple[bool, ResourceKey | Exception]:
    try:
        return True, lift_resource_key(value)
    except Exception as e:
        return False, e


ScopeKey = Union[ProcessInstanceKey, ElementInstanceKey]


def lift_scope_key(value: Any) -> ScopeKey:
    try:
        return lift_process_instance_key(value)
    except Exception:
        pass
    try:
        return lift_element_instance_key(value)
    except Exception:
        pass
    raise ValueError(
        f"ScopeKey: value {value!r} does not match any branch (ProcessInstanceKey, ElementInstanceKey)"
    )


def try_lift_scope_key(value: Any) -> Tuple[bool, ScopeKey | Exception]:
    try:
        return True, lift_scope_key(value)
    except Exception as e:
        return False, e


__all__ = [
    "AuditLogEntityKey",
    "AuditLogKey",
    "AuthorizationKey",
    "BatchOperationKey",
    "BusinessId",
    "ConditionalEvaluationKey",
    "DecisionDefinitionId",
    "DecisionDefinitionKey",
    "DecisionEvaluationInstanceKey",
    "DecisionEvaluationKey",
    "DecisionInstanceKey",
    "DecisionRequirementsKey",
    "DeploymentKey",
    "DocumentId",
    "ElementId",
    "ElementInstanceKey",
    "EndCursor",
    "FormId",
    "FormKey",
    "GlobalListenerId",
    "IncidentKey",
    "JobKey",
    "MessageKey",
    "MessageSubscriptionKey",
    "ProcessDefinitionId",
    "ProcessDefinitionKey",
    "ProcessInstanceKey",
    "ResourceKey",
    "ScopeKey",
    "SignalKey",
    "StartCursor",
    "Tag",
    "TenantId",
    "UserTaskKey",
    "Username",
    "VariableKey",
    "lift_audit_log_entity_key",
    "lift_audit_log_key",
    "lift_authorization_key",
    "lift_batch_operation_key",
    "lift_business_id",
    "lift_conditional_evaluation_key",
    "lift_decision_definition_id",
    "lift_decision_definition_key",
    "lift_decision_evaluation_instance_key",
    "lift_decision_evaluation_key",
    "lift_decision_instance_key",
    "lift_decision_requirements_key",
    "lift_deployment_key",
    "lift_document_id",
    "lift_element_id",
    "lift_element_instance_key",
    "lift_end_cursor",
    "lift_form_id",
    "lift_form_key",
    "lift_global_listener_id",
    "lift_incident_key",
    "lift_job_key",
    "lift_message_key",
    "lift_message_subscription_key",
    "lift_process_definition_id",
    "lift_process_definition_key",
    "lift_process_instance_key",
    "lift_resource_key",
    "lift_scope_key",
    "lift_signal_key",
    "lift_start_cursor",
    "lift_tag",
    "lift_tenant_id",
    "lift_user_task_key",
    "lift_username",
    "lift_variable_key",
    "try_lift_audit_log_entity_key",
    "try_lift_audit_log_key",
    "try_lift_authorization_key",
    "try_lift_batch_operation_key",
    "try_lift_business_id",
    "try_lift_conditional_evaluation_key",
    "try_lift_decision_definition_id",
    "try_lift_decision_definition_key",
    "try_lift_decision_evaluation_instance_key",
    "try_lift_decision_evaluation_key",
    "try_lift_decision_instance_key",
    "try_lift_decision_requirements_key",
    "try_lift_deployment_key",
    "try_lift_document_id",
    "try_lift_element_id",
    "try_lift_element_instance_key",
    "try_lift_end_cursor",
    "try_lift_form_id",
    "try_lift_form_key",
    "try_lift_global_listener_id",
    "try_lift_incident_key",
    "try_lift_job_key",
    "try_lift_message_key",
    "try_lift_message_subscription_key",
    "try_lift_process_definition_id",
    "try_lift_process_definition_key",
    "try_lift_process_instance_key",
    "try_lift_resource_key",
    "try_lift_scope_key",
    "try_lift_signal_key",
    "try_lift_start_cursor",
    "try_lift_tag",
    "try_lift_tenant_id",
    "try_lift_user_task_key",
    "try_lift_username",
    "try_lift_variable_key",
]
