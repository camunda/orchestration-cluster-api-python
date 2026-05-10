from __future__ import annotations
from typing import Any, Tuple, Union
import re


class AgentInstanceKey(str):
    def __new__(cls, value: str) -> "AgentInstanceKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"AgentInstanceKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^-?[0-9]+$", value) is None:
            pat = "^-?[0-9]+$"
            raise ValueError(
                f"AgentInstanceKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"AgentInstanceKey shorter than minLength 1, got {value!r}"
            )
        if len(value) > 25:
            raise ValueError(
                f"AgentInstanceKey longer than maxLength 25, got {value!r}"
            )
        return super().__new__(cls, value)


class AuditLogEntityKey(str):
    def __new__(cls, value: str) -> "AuditLogEntityKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"AuditLogEntityKey must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


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


class BatchOperationKey(str):
    def __new__(cls, value: str) -> "BatchOperationKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"BatchOperationKey must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


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


class ClientId(str):
    def __new__(cls, value: str) -> "ClientId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ClientId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[a-zA-Z0-9_~@.+-]+$", value) is None:
            pat = "^[a-zA-Z0-9_~@.+-]+$"
            raise ValueError(f"ClientId does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"ClientId shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"ClientId longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


class ClusterVariableName(str):
    def __new__(cls, value: str) -> "ClusterVariableName":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ClusterVariableName must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[a-zA-Z0-9_~@.+-]+$", value) is None:
            pat = "^[a-zA-Z0-9_~@.+-]+$"
            raise ValueError(
                f"ClusterVariableName does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"ClusterVariableName shorter than minLength 1, got {value!r}"
            )
        if len(value) > 256:
            raise ValueError(
                f"ClusterVariableName longer than maxLength 256, got {value!r}"
            )
        return super().__new__(cls, value)


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


class DecisionEvaluationInstanceKey(str):
    def __new__(cls, value: str) -> "DecisionEvaluationInstanceKey":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DecisionEvaluationInstanceKey must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[0-9]+-[0-9]+$", value) is None:
            pat = "^[0-9]+-[0-9]+$"
            raise ValueError(
                f"DecisionEvaluationInstanceKey does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 3:
            raise ValueError(
                f"DecisionEvaluationInstanceKey shorter than minLength 3, got {value!r}"
            )
        if len(value) > 30:
            raise ValueError(
                f"DecisionEvaluationInstanceKey longer than maxLength 30, got {value!r}"
            )
        return super().__new__(cls, value)


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


class DocumentId(str):
    def __new__(cls, value: str) -> "DocumentId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"DocumentId must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


class ElementId(str):
    def __new__(cls, value: str) -> "ElementId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"ElementId must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


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


class FormId(str):
    def __new__(cls, value: str) -> "FormId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"FormId must be str, got {type(value).__name__}: {value!r}"
            )
        return super().__new__(cls, value)


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


class GlobalListenerId(str):
    def __new__(cls, value: str) -> "GlobalListenerId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"GlobalListenerId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[a-zA-Z0-9_~@.+\\-]+$", value) is None:
            pat = "^[a-zA-Z0-9_~@.+\\-]+$"
            raise ValueError(
                f"GlobalListenerId does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(
                f"GlobalListenerId shorter than minLength 1, got {value!r}"
            )
        if len(value) > 256:
            raise ValueError(
                f"GlobalListenerId longer than maxLength 256, got {value!r}"
            )
        return super().__new__(cls, value)


class GroupId(str):
    def __new__(cls, value: str) -> "GroupId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"GroupId must be str, got {type(value).__name__}: {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"GroupId shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"GroupId longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


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


class MappingRuleId(str):
    def __new__(cls, value: str) -> "MappingRuleId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"MappingRuleId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[a-zA-Z0-9_~@.+-]+$", value) is None:
            pat = "^[a-zA-Z0-9_~@.+-]+$"
            raise ValueError(
                f"MappingRuleId does not match pattern {pat!r}, got {value!r}"
            )
        if len(value) < 1:
            raise ValueError(f"MappingRuleId shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"MappingRuleId longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


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


class RoleId(str):
    def __new__(cls, value: str) -> "RoleId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"RoleId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[a-zA-Z0-9_~@.+-]+$", value) is None:
            pat = "^[a-zA-Z0-9_~@.+-]+$"
            raise ValueError(f"RoleId does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"RoleId shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"RoleId longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


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


class TenantId(str):
    def __new__(cls, value: str) -> "TenantId":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"TenantId must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^(<default>|[\\w\\.\\-]{1,31})$", value) is None:
            pat = "^(<default>|[\\w\\.\\-]{1,31})$"
            raise ValueError(f"TenantId does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"TenantId shorter than minLength 1, got {value!r}")
        if len(value) > 31:
            raise ValueError(f"TenantId longer than maxLength 31, got {value!r}")
        return super().__new__(cls, value)


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


class Username(str):
    def __new__(cls, value: str) -> "Username":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"Username must be str, got {type(value).__name__}: {value!r}"
            )
        if re.fullmatch("^[a-zA-Z0-9_~@.+-]+$", value) is None:
            pat = "^[a-zA-Z0-9_~@.+-]+$"
            raise ValueError(f"Username does not match pattern {pat!r}, got {value!r}")
        if len(value) < 1:
            raise ValueError(f"Username shorter than minLength 1, got {value!r}")
        if len(value) > 256:
            raise ValueError(f"Username longer than maxLength 256, got {value!r}")
        return super().__new__(cls, value)


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


ResourceKey = Union[
    ProcessDefinitionKey, DecisionRequirementsKey, FormKey, DecisionDefinitionKey
]


def lift_resource_key(value: Any) -> ResourceKey:
    try:
        return ProcessDefinitionKey(value)
    except Exception:
        pass
    try:
        return DecisionRequirementsKey(value)
    except Exception:
        pass
    try:
        return FormKey(value)
    except Exception:
        pass
    try:
        return DecisionDefinitionKey(value)
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
        return ProcessInstanceKey(value)
    except Exception:
        pass
    try:
        return ElementInstanceKey(value)
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
    "AgentInstanceKey",
    "AuditLogEntityKey",
    "AuditLogKey",
    "AuthorizationKey",
    "BatchOperationKey",
    "BusinessId",
    "ClientId",
    "ClusterVariableName",
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
    "GroupId",
    "IncidentKey",
    "JobKey",
    "MappingRuleId",
    "MessageKey",
    "MessageSubscriptionKey",
    "ProcessDefinitionId",
    "ProcessDefinitionKey",
    "ProcessInstanceKey",
    "ResourceKey",
    "RoleId",
    "ScopeKey",
    "SignalKey",
    "StartCursor",
    "Tag",
    "TenantId",
    "UserTaskKey",
    "Username",
    "VariableKey",
    "lift_resource_key",
    "lift_scope_key",
    "try_lift_resource_key",
    "try_lift_scope_key",
]
