from __future__ import annotations
from typing import NewType, Any, Tuple
import re

AuditLogEntityKey = NewType("AuditLogEntityKey", str)


def lift_audit_log_entity_key(value: Any) -> AuditLogEntityKey:
    if not isinstance(value, str):
        raise TypeError(
            f"AuditLogEntityKey must be str, got {type(value).__name__}: {value!r}"
        )
    return AuditLogEntityKey(value)


def try_lift_audit_log_entity_key(
    value: Any,
) -> Tuple[bool, AuditLogEntityKey | Exception]:
    try:
        return True, lift_audit_log_entity_key(value)
    except Exception as e:
        return False, e


AuditLogKey = NewType("AuditLogKey", str)


def lift_audit_log_key(value: Any) -> AuditLogKey:
    if not isinstance(value, str):
        raise TypeError(
            f"AuditLogKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"AuditLogKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"AuditLogKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"AuditLogKey longer than maxLength 25, got {value!r}")
    return AuditLogKey(value)


def try_lift_audit_log_key(value: Any) -> Tuple[bool, AuditLogKey | Exception]:
    try:
        return True, lift_audit_log_key(value)
    except Exception as e:
        return False, e


AuthorizationKey = NewType("AuthorizationKey", str)


def lift_authorization_key(value: Any) -> AuthorizationKey:
    if not isinstance(value, str):
        raise TypeError(
            f"AuthorizationKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"AuthorizationKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"AuthorizationKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"AuthorizationKey longer than maxLength 25, got {value!r}")
    return AuthorizationKey(value)


def try_lift_authorization_key(value: Any) -> Tuple[bool, AuthorizationKey | Exception]:
    try:
        return True, lift_authorization_key(value)
    except Exception as e:
        return False, e


BatchOperationKey = NewType("BatchOperationKey", str)


def lift_batch_operation_key(value: Any) -> BatchOperationKey:
    if not isinstance(value, str):
        raise TypeError(
            f"BatchOperationKey must be str, got {type(value).__name__}: {value!r}"
        )
    return BatchOperationKey(value)


def try_lift_batch_operation_key(
    value: Any,
) -> Tuple[bool, BatchOperationKey | Exception]:
    try:
        return True, lift_batch_operation_key(value)
    except Exception as e:
        return False, e


ConditionalEvaluationKey = NewType("ConditionalEvaluationKey", str)


def lift_conditional_evaluation_key(value: Any) -> ConditionalEvaluationKey:
    if not isinstance(value, str):
        raise TypeError(
            f"ConditionalEvaluationKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"ConditionalEvaluationKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"ConditionalEvaluationKey shorter than minLength 1, got {value!r}"
        )
    if len(value) > 25:
        raise ValueError(
            f"ConditionalEvaluationKey longer than maxLength 25, got {value!r}"
        )
    return ConditionalEvaluationKey(value)


def try_lift_conditional_evaluation_key(
    value: Any,
) -> Tuple[bool, ConditionalEvaluationKey | Exception]:
    try:
        return True, lift_conditional_evaluation_key(value)
    except Exception as e:
        return False, e


DecisionDefinitionId = NewType("DecisionDefinitionId", str)


def lift_decision_definition_id(value: Any) -> DecisionDefinitionId:
    if not isinstance(value, str):
        raise TypeError(
            f"DecisionDefinitionId must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^[A-Za-z0-9_@.+-]+$", value) is None:
        raise ValueError(
            f"DecisionDefinitionId does not match pattern '^[A-Za-z0-9_@.+-]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"DecisionDefinitionId shorter than minLength 1, got {value!r}"
        )
    if len(value) > 256:
        raise ValueError(
            f"DecisionDefinitionId longer than maxLength 256, got {value!r}"
        )
    return DecisionDefinitionId(value)


def try_lift_decision_definition_id(
    value: Any,
) -> Tuple[bool, DecisionDefinitionId | Exception]:
    try:
        return True, lift_decision_definition_id(value)
    except Exception as e:
        return False, e


DecisionDefinitionKey = NewType("DecisionDefinitionKey", str)


def lift_decision_definition_key(value: Any) -> DecisionDefinitionKey:
    if not isinstance(value, str):
        raise TypeError(
            f"DecisionDefinitionKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"DecisionDefinitionKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"DecisionDefinitionKey shorter than minLength 1, got {value!r}"
        )
    if len(value) > 25:
        raise ValueError(
            f"DecisionDefinitionKey longer than maxLength 25, got {value!r}"
        )
    return DecisionDefinitionKey(value)


def try_lift_decision_definition_key(
    value: Any,
) -> Tuple[bool, DecisionDefinitionKey | Exception]:
    try:
        return True, lift_decision_definition_key(value)
    except Exception as e:
        return False, e


DecisionEvaluationInstanceKey = NewType("DecisionEvaluationInstanceKey", str)


def lift_decision_evaluation_instance_key(value: Any) -> DecisionEvaluationInstanceKey:
    if not isinstance(value, str):
        raise TypeError(
            f"DecisionEvaluationInstanceKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"DecisionEvaluationInstanceKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"DecisionEvaluationInstanceKey shorter than minLength 1, got {value!r}"
        )
    if len(value) > 25:
        raise ValueError(
            f"DecisionEvaluationInstanceKey longer than maxLength 25, got {value!r}"
        )
    return DecisionEvaluationInstanceKey(value)


def try_lift_decision_evaluation_instance_key(
    value: Any,
) -> Tuple[bool, DecisionEvaluationInstanceKey | Exception]:
    try:
        return True, lift_decision_evaluation_instance_key(value)
    except Exception as e:
        return False, e


DecisionEvaluationKey = NewType("DecisionEvaluationKey", str)


def lift_decision_evaluation_key(value: Any) -> DecisionEvaluationKey:
    if not isinstance(value, str):
        raise TypeError(
            f"DecisionEvaluationKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"DecisionEvaluationKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"DecisionEvaluationKey shorter than minLength 1, got {value!r}"
        )
    if len(value) > 25:
        raise ValueError(
            f"DecisionEvaluationKey longer than maxLength 25, got {value!r}"
        )
    return DecisionEvaluationKey(value)


def try_lift_decision_evaluation_key(
    value: Any,
) -> Tuple[bool, DecisionEvaluationKey | Exception]:
    try:
        return True, lift_decision_evaluation_key(value)
    except Exception as e:
        return False, e


DecisionInstanceKey = NewType("DecisionInstanceKey", str)


def lift_decision_instance_key(value: Any) -> DecisionInstanceKey:
    if not isinstance(value, str):
        raise TypeError(
            f"DecisionInstanceKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"DecisionInstanceKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"DecisionInstanceKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"DecisionInstanceKey longer than maxLength 25, got {value!r}")
    return DecisionInstanceKey(value)


def try_lift_decision_instance_key(
    value: Any,
) -> Tuple[bool, DecisionInstanceKey | Exception]:
    try:
        return True, lift_decision_instance_key(value)
    except Exception as e:
        return False, e


DecisionRequirementsKey = NewType("DecisionRequirementsKey", str)


def lift_decision_requirements_key(value: Any) -> DecisionRequirementsKey:
    if not isinstance(value, str):
        raise TypeError(
            f"DecisionRequirementsKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"DecisionRequirementsKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"DecisionRequirementsKey shorter than minLength 1, got {value!r}"
        )
    if len(value) > 25:
        raise ValueError(
            f"DecisionRequirementsKey longer than maxLength 25, got {value!r}"
        )
    return DecisionRequirementsKey(value)


def try_lift_decision_requirements_key(
    value: Any,
) -> Tuple[bool, DecisionRequirementsKey | Exception]:
    try:
        return True, lift_decision_requirements_key(value)
    except Exception as e:
        return False, e


DeploymentKey = NewType("DeploymentKey", str)


def lift_deployment_key(value: Any) -> DeploymentKey:
    if not isinstance(value, str):
        raise TypeError(
            f"DeploymentKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"DeploymentKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"DeploymentKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"DeploymentKey longer than maxLength 25, got {value!r}")
    return DeploymentKey(value)


def try_lift_deployment_key(value: Any) -> Tuple[bool, DeploymentKey | Exception]:
    try:
        return True, lift_deployment_key(value)
    except Exception as e:
        return False, e


DocumentId = NewType("DocumentId", str)


def lift_document_id(value: Any) -> DocumentId:
    if not isinstance(value, str):
        raise TypeError(
            f"DocumentId must be str, got {type(value).__name__}: {value!r}"
        )
    return DocumentId(value)


def try_lift_document_id(value: Any) -> Tuple[bool, DocumentId | Exception]:
    try:
        return True, lift_document_id(value)
    except Exception as e:
        return False, e


ElementId = NewType("ElementId", str)


def lift_element_id(value: Any) -> ElementId:
    if not isinstance(value, str):
        raise TypeError(f"ElementId must be str, got {type(value).__name__}: {value!r}")
    return ElementId(value)


def try_lift_element_id(value: Any) -> Tuple[bool, ElementId | Exception]:
    try:
        return True, lift_element_id(value)
    except Exception as e:
        return False, e


ElementInstanceKey = NewType("ElementInstanceKey", str)


def lift_element_instance_key(value: Any) -> ElementInstanceKey:
    if not isinstance(value, str):
        raise TypeError(
            f"ElementInstanceKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"ElementInstanceKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"ElementInstanceKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"ElementInstanceKey longer than maxLength 25, got {value!r}")
    return ElementInstanceKey(value)


def try_lift_element_instance_key(
    value: Any,
) -> Tuple[bool, ElementInstanceKey | Exception]:
    try:
        return True, lift_element_instance_key(value)
    except Exception as e:
        return False, e


EndCursor = NewType("EndCursor", str)


def lift_end_cursor(value: Any) -> EndCursor:
    if not isinstance(value, str):
        raise TypeError(f"EndCursor must be str, got {type(value).__name__}: {value!r}")
    if (
        re.fullmatch(
            r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$",
            value,
        )
        is None
    ):
        raise ValueError(
            f"EndCursor does not match pattern '^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$', got {value!r}"
        )
    if len(value) < 2:
        raise ValueError(f"EndCursor shorter than minLength 2, got {value!r}")
    if len(value) > 300:
        raise ValueError(f"EndCursor longer than maxLength 300, got {value!r}")
    return EndCursor(value)


def try_lift_end_cursor(value: Any) -> Tuple[bool, EndCursor | Exception]:
    try:
        return True, lift_end_cursor(value)
    except Exception as e:
        return False, e


FormId = NewType("FormId", str)


def lift_form_id(value: Any) -> FormId:
    if not isinstance(value, str):
        raise TypeError(f"FormId must be str, got {type(value).__name__}: {value!r}")
    return FormId(value)


def try_lift_form_id(value: Any) -> Tuple[bool, FormId | Exception]:
    try:
        return True, lift_form_id(value)
    except Exception as e:
        return False, e


FormKey = NewType("FormKey", str)


def lift_form_key(value: Any) -> FormKey:
    if not isinstance(value, str):
        raise TypeError(f"FormKey must be str, got {type(value).__name__}: {value!r}")
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(f"FormKey does not match pattern '^-?[0-9]+$', got {value!r}")
    if len(value) < 1:
        raise ValueError(f"FormKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"FormKey longer than maxLength 25, got {value!r}")
    return FormKey(value)


def try_lift_form_key(value: Any) -> Tuple[bool, FormKey | Exception]:
    try:
        return True, lift_form_key(value)
    except Exception as e:
        return False, e


IncidentKey = NewType("IncidentKey", str)


def lift_incident_key(value: Any) -> IncidentKey:
    if not isinstance(value, str):
        raise TypeError(
            f"IncidentKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"IncidentKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"IncidentKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"IncidentKey longer than maxLength 25, got {value!r}")
    return IncidentKey(value)


def try_lift_incident_key(value: Any) -> Tuple[bool, IncidentKey | Exception]:
    try:
        return True, lift_incident_key(value)
    except Exception as e:
        return False, e


JobKey = NewType("JobKey", str)


def lift_job_key(value: Any) -> JobKey:
    if not isinstance(value, str):
        raise TypeError(f"JobKey must be str, got {type(value).__name__}: {value!r}")
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(f"JobKey does not match pattern '^-?[0-9]+$', got {value!r}")
    if len(value) < 1:
        raise ValueError(f"JobKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"JobKey longer than maxLength 25, got {value!r}")
    return JobKey(value)


def try_lift_job_key(value: Any) -> Tuple[bool, JobKey | Exception]:
    try:
        return True, lift_job_key(value)
    except Exception as e:
        return False, e


MessageKey = NewType("MessageKey", str)


def lift_message_key(value: Any) -> MessageKey:
    if not isinstance(value, str):
        raise TypeError(
            f"MessageKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"MessageKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"MessageKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"MessageKey longer than maxLength 25, got {value!r}")
    return MessageKey(value)


def try_lift_message_key(value: Any) -> Tuple[bool, MessageKey | Exception]:
    try:
        return True, lift_message_key(value)
    except Exception as e:
        return False, e


MessageSubscriptionKey = NewType("MessageSubscriptionKey", str)


def lift_message_subscription_key(value: Any) -> MessageSubscriptionKey:
    if not isinstance(value, str):
        raise TypeError(
            f"MessageSubscriptionKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"MessageSubscriptionKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"MessageSubscriptionKey shorter than minLength 1, got {value!r}"
        )
    if len(value) > 25:
        raise ValueError(
            f"MessageSubscriptionKey longer than maxLength 25, got {value!r}"
        )
    return MessageSubscriptionKey(value)


def try_lift_message_subscription_key(
    value: Any,
) -> Tuple[bool, MessageSubscriptionKey | Exception]:
    try:
        return True, lift_message_subscription_key(value)
    except Exception as e:
        return False, e


ProcessDefinitionId = NewType("ProcessDefinitionId", str)


def lift_process_definition_id(value: Any) -> ProcessDefinitionId:
    if not isinstance(value, str):
        raise TypeError(
            f"ProcessDefinitionId must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_\\-\\.]*$", value) is None:
        raise ValueError(
            f"ProcessDefinitionId does not match pattern '^[a-zA-Z_][a-zA-Z0-9_\\-\\.]*$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"ProcessDefinitionId shorter than minLength 1, got {value!r}")
    return ProcessDefinitionId(value)


def try_lift_process_definition_id(
    value: Any,
) -> Tuple[bool, ProcessDefinitionId | Exception]:
    try:
        return True, lift_process_definition_id(value)
    except Exception as e:
        return False, e


ProcessDefinitionKey = NewType("ProcessDefinitionKey", str)


def lift_process_definition_key(value: Any) -> ProcessDefinitionKey:
    if not isinstance(value, str):
        raise TypeError(
            f"ProcessDefinitionKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"ProcessDefinitionKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(
            f"ProcessDefinitionKey shorter than minLength 1, got {value!r}"
        )
    if len(value) > 25:
        raise ValueError(
            f"ProcessDefinitionKey longer than maxLength 25, got {value!r}"
        )
    return ProcessDefinitionKey(value)


def try_lift_process_definition_key(
    value: Any,
) -> Tuple[bool, ProcessDefinitionKey | Exception]:
    try:
        return True, lift_process_definition_key(value)
    except Exception as e:
        return False, e


ProcessInstanceKey = NewType("ProcessInstanceKey", str)


def lift_process_instance_key(value: Any) -> ProcessInstanceKey:
    if not isinstance(value, str):
        raise TypeError(
            f"ProcessInstanceKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"ProcessInstanceKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"ProcessInstanceKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"ProcessInstanceKey longer than maxLength 25, got {value!r}")
    return ProcessInstanceKey(value)


def try_lift_process_instance_key(
    value: Any,
) -> Tuple[bool, ProcessInstanceKey | Exception]:
    try:
        return True, lift_process_instance_key(value)
    except Exception as e:
        return False, e


ScopeKey = NewType("ScopeKey", str)


def lift_scope_key(value: Any) -> ScopeKey:
    if not isinstance(value, str):
        raise TypeError(f"ScopeKey must be str, got {type(value).__name__}: {value!r}")
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(f"ScopeKey does not match pattern '^-?[0-9]+$', got {value!r}")
    if len(value) < 1:
        raise ValueError(f"ScopeKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"ScopeKey longer than maxLength 25, got {value!r}")
    return ScopeKey(value)


def try_lift_scope_key(value: Any) -> Tuple[bool, ScopeKey | Exception]:
    try:
        return True, lift_scope_key(value)
    except Exception as e:
        return False, e


SignalKey = NewType("SignalKey", str)


def lift_signal_key(value: Any) -> SignalKey:
    if not isinstance(value, str):
        raise TypeError(f"SignalKey must be str, got {type(value).__name__}: {value!r}")
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"SignalKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"SignalKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"SignalKey longer than maxLength 25, got {value!r}")
    return SignalKey(value)


def try_lift_signal_key(value: Any) -> Tuple[bool, SignalKey | Exception]:
    try:
        return True, lift_signal_key(value)
    except Exception as e:
        return False, e


StartCursor = NewType("StartCursor", str)


def lift_start_cursor(value: Any) -> StartCursor:
    if not isinstance(value, str):
        raise TypeError(
            f"StartCursor must be str, got {type(value).__name__}: {value!r}"
        )
    if (
        re.fullmatch(
            r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$",
            value,
        )
        is None
    ):
        raise ValueError(
            f"StartCursor does not match pattern '^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}(?:==)?|[A-Za-z0-9+/]{3}=)?$', got {value!r}"
        )
    if len(value) < 2:
        raise ValueError(f"StartCursor shorter than minLength 2, got {value!r}")
    if len(value) > 300:
        raise ValueError(f"StartCursor longer than maxLength 300, got {value!r}")
    return StartCursor(value)


def try_lift_start_cursor(value: Any) -> Tuple[bool, StartCursor | Exception]:
    try:
        return True, lift_start_cursor(value)
    except Exception as e:
        return False, e


Tag = NewType("Tag", str)


def lift_tag(value: Any) -> Tag:
    if not isinstance(value, str):
        raise TypeError(f"Tag must be str, got {type(value).__name__}: {value!r}")
    if re.fullmatch(r"^[A-Za-z][A-Za-z0-9_\\-:.]{0,99}$", value) is None:
        raise ValueError(
            f"Tag does not match pattern '^[A-Za-z][A-Za-z0-9_\\-:.]{0, 99}$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"Tag shorter than minLength 1, got {value!r}")
    if len(value) > 100:
        raise ValueError(f"Tag longer than maxLength 100, got {value!r}")
    return Tag(value)


def try_lift_tag(value: Any) -> Tuple[bool, Tag | Exception]:
    try:
        return True, lift_tag(value)
    except Exception as e:
        return False, e


TenantId = NewType("TenantId", str)


def lift_tenant_id(value: Any) -> TenantId:
    if not isinstance(value, str):
        raise TypeError(f"TenantId must be str, got {type(value).__name__}: {value!r}")
    if re.fullmatch(r"^(<default>|[A-Za-z0-9_@.+-]+)$", value) is None:
        raise ValueError(
            f"TenantId does not match pattern '^(<default>|[A-Za-z0-9_@.+-]+)$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"TenantId shorter than minLength 1, got {value!r}")
    if len(value) > 256:
        raise ValueError(f"TenantId longer than maxLength 256, got {value!r}")
    return TenantId(value)


def try_lift_tenant_id(value: Any) -> Tuple[bool, TenantId | Exception]:
    try:
        return True, lift_tenant_id(value)
    except Exception as e:
        return False, e


UserTaskKey = NewType("UserTaskKey", str)


def lift_user_task_key(value: Any) -> UserTaskKey:
    if not isinstance(value, str):
        raise TypeError(
            f"UserTaskKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"UserTaskKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"UserTaskKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"UserTaskKey longer than maxLength 25, got {value!r}")
    return UserTaskKey(value)


def try_lift_user_task_key(value: Any) -> Tuple[bool, UserTaskKey | Exception]:
    try:
        return True, lift_user_task_key(value)
    except Exception as e:
        return False, e


Username = NewType("Username", str)


def lift_username(value: Any) -> Username:
    if not isinstance(value, str):
        raise TypeError(f"Username must be str, got {type(value).__name__}: {value!r}")
    if re.fullmatch(r"^(<default>|[A-Za-z0-9_@.+-]+)$", value) is None:
        raise ValueError(
            f"Username does not match pattern '^(<default>|[A-Za-z0-9_@.+-]+)$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"Username shorter than minLength 1, got {value!r}")
    if len(value) > 256:
        raise ValueError(f"Username longer than maxLength 256, got {value!r}")
    return Username(value)


def try_lift_username(value: Any) -> Tuple[bool, Username | Exception]:
    try:
        return True, lift_username(value)
    except Exception as e:
        return False, e


VariableKey = NewType("VariableKey", str)


def lift_variable_key(value: Any) -> VariableKey:
    if not isinstance(value, str):
        raise TypeError(
            f"VariableKey must be str, got {type(value).__name__}: {value!r}"
        )
    if re.fullmatch(r"^-?[0-9]+$", value) is None:
        raise ValueError(
            f"VariableKey does not match pattern '^-?[0-9]+$', got {value!r}"
        )
    if len(value) < 1:
        raise ValueError(f"VariableKey shorter than minLength 1, got {value!r}")
    if len(value) > 25:
        raise ValueError(f"VariableKey longer than maxLength 25, got {value!r}")
    return VariableKey(value)


def try_lift_variable_key(value: Any) -> Tuple[bool, VariableKey | Exception]:
    try:
        return True, lift_variable_key(value)
    except Exception as e:
        return False, e


__all__ = [
    "AuditLogEntityKey",
    "AuditLogKey",
    "AuthorizationKey",
    "BatchOperationKey",
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
    "IncidentKey",
    "JobKey",
    "MessageKey",
    "MessageSubscriptionKey",
    "ProcessDefinitionId",
    "ProcessDefinitionKey",
    "ProcessInstanceKey",
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
    "lift_incident_key",
    "lift_job_key",
    "lift_message_key",
    "lift_message_subscription_key",
    "lift_process_definition_id",
    "lift_process_definition_key",
    "lift_process_instance_key",
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
    "try_lift_incident_key",
    "try_lift_job_key",
    "try_lift_message_key",
    "try_lift_message_subscription_key",
    "try_lift_process_definition_id",
    "try_lift_process_definition_key",
    "try_lift_process_instance_key",
    "try_lift_scope_key",
    "try_lift_signal_key",
    "try_lift_start_cursor",
    "try_lift_tag",
    "try_lift_tenant_id",
    "try_lift_user_task_key",
    "try_lift_username",
    "try_lift_variable_key",
]
